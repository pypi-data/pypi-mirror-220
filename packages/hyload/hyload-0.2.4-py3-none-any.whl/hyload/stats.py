from hyload.util import getCurTime
import time,sys,json,socket,os,gevent
import http.client
from urllib.parse import quote_plus
from .logger import TestLogger
from typing import Union

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getCommandArg(argName):
    for arg in sys.argv[1:]:
        if f'{argName}=' in arg:
            value = arg.replace(f'{argName}=','')
            return value
    
    return None

# 控制台程序地址
ConsoleAddr = getCommandArg('console')

# 统计数据文件
StatsFile = getCommandArg('statsfile')

if ConsoleAddr:
    # print (f'Console addr:{ConsoleAddr}')
    # consoleConnection = http.client.HTTPConnection(
    #                             ConsoleAddr,  #ConsoleAddr 'httpbin.org'
    #                             timeout=0.3)

    # Create a UDP socket at client side

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    parts = ConsoleAddr.split(':')
    UDPServerAddr = parts[0],int(parts[1])
    # print(UDPServerAddr)

if StatsFile:
    statsDir = os.path.dirname(StatsFile)
    if statsDir:
        os.makedirs(statsDir,exist_ok=True)
    foStats = open(StatsFile,'wb')

class Stats:
    
    @staticmethod
    def wait_for_tasks_done(tasks:list=None):
        gevent.wait(tasks) # wait for tasks end
        time.sleep(1) # wait for stats routine to send last second stats
        print('\n==== 运行结束 ====')

    @classmethod
    def clear(cls):
        cls.startTime = getCurTime()

        cls.connectionNumber = 0 # 连接数量统计

        # 累积统计
        cls.totalSend = 0
        cls.totalRecv = 0
        cls.totalTimeout = 0
        cls.totalError = 0

        # 每秒统计数据
        cls.rpsTable = {}
        cls.tpsTable = {}
        cls.responseTimeTable = {}
        cls.timeoutTable = {}
        cls.errorTable = {}        
        # 响应时长区段统计
        cls.resptimeRange ={
            '<100ms':      0,
            '100-500ms':   0,
            '500-1000ms':  0,
            '1000-3000ms': 0,
            '>=3000ms':    0,
        } 

        # # 记录是否有待处理的
        # hasStatsForSeconds  = {}
        
        cls.runFlag = False

        cls.logFh = None


    @classmethod
    def _sendStatsToConsoleTcp(cls, stats):
        if not ConsoleAddr:
            return
            
        consoleConnection = http.client.HTTPConnection(
                            ConsoleAddr,  #ConsoleAddr 'httpbin.org'
                            timeout=5)

        # print('send request to console----------')
        try:
            consoleConnection.request('GET', 
                     '/stats?value=' + quote_plus(json.dumps(stats)), 
                     
                    #  '/get?'+ quote_plus(json.dumps(stats).encode()), 
                     body=None,
                     headers={
                            'User-Agent' : "BYLOAD TESTER"
                        })                
            
            httpResponse = consoleConnection.getresponse()
            
            httpResponse.close()

        except Exception as e:
            print(f'send stats to console failed! {e}')


    @classmethod
    def _sendStatsToConsoleUdp(cls, statsBytes):
        if not ConsoleAddr:
            return
                       
        
        # print('send request to console----------')
        try:
            UDPClientSocket.sendto(
                statsBytes,
                UDPServerAddr)                
                            

        except Exception as e:
            print(f'send stats to console failed! {e}')


    @classmethod
    def _statsOneTable(cls,
                       strLastSecond,
                      lastSecond,
                      table,
                      tableName,
                      action,
                      statsOneSecond):

        # 如果前1秒 有记录， 打印出记录，并且加入发送给console的信息里
        if lastSecond in table:
            if cls.runFlag:
                print(f'{strLastSecond} {action} {table[lastSecond]:6}')
            statsOneSecond[tableName] = table[lastSecond]
            table.pop(lastSecond)
        else:
            statsOneSecond[tableName] = 0


    # 一秒结束后的统计处理
    @classmethod
    def _one_second_data_done_stats(cls,lastSecond):
        strLastSecond = time.strftime('%H:%M:%S',time.localtime(lastSecond))
         
        # 如果上一秒没有什么有效信息
        # 表示 要么是上1秒没有收发数据也没有超时错误，要么是 上1秒的统计已经发送出去 
        # 这次都不需要发送统计
        if (lastSecond not in cls.rpsTable) and \
            (lastSecond not in cls.tpsTable) and \
            (lastSecond not in cls.timeoutTable) and \
            (lastSecond not in cls.errorTable):     
            return   

            
        # 如果上1秒统计数据存在，表示上1秒的数据还没有发送出去   
        
        # 创建统计数据对象
        statsOneSecond = {'t':lastSecond}

        # rps
        cls._statsOneTable(strLastSecond,lastSecond,cls.rpsTable,'rps','send',statsOneSecond)

        # tops
        cls._statsOneTable(strLastSecond,lastSecond,cls.timeoutTable,'tops','timeout',statsOneSecond)

        # eps
        cls._statsOneTable(strLastSecond,lastSecond,cls.errorTable, 'eps','error',statsOneSecond)

        # tps、respTimeSum 、 avgRespTime
        if lastSecond in cls.tpsTable:
            count = cls.tpsTable[lastSecond]
            avgRespTime = cls.responseTimeTable[lastSecond]/count  
            if cls.runFlag:
                print(f'{strLastSecond} recv {count:6} | avg lantency {avgRespTime:.4f}')

            statsOneSecond['tps'] = count
            statsOneSecond['respTimeSum'] = round(cls.responseTimeTable[lastSecond],4)
            statsOneSecond['avgRespTime'] = round(avgRespTime,4)

            cls.tpsTable.pop(lastSecond)
            cls.responseTimeTable.pop(lastSecond)
        else:
            statsOneSecond['tps'] = 0
            statsOneSecond['respTimeSum'] = 0
            statsOneSecond['avgRespTime'] = 0




        # 如果没有信息，这次不需要发送统计
        if len(statsOneSecond) == 1:
            return

        # 否则加上 累计汇总 统计信息，一起发出去
        total = {}
        total['send'] = cls.totalSend
        total['recv'] = cls.totalRecv

        if  cls.totalTimeout > 0 :
            total['timeout'] = cls.totalTimeout
        if  cls.totalError > 0 :
            total['error'] = cls.totalError

        # 响应时长区段统计，去掉为0的            
        total.update({ tr:count  for tr,count in  cls.resptimeRange.items() if count>0})

        statsOneSecond['total'] = total
        
        
        # 统计对象数据序列化为字节
        statsBytes = json.dumps(statsOneSecond).encode()

        # 发给console集中显示
        if ConsoleAddr:
            cls._sendStatsToConsoleUdp(statsBytes)

        if StatsFile:
            foStats.write(statsBytes+b'\n')
            foStats.flush()

        # 发送到 console的 并发连接数量 数据
        # 目前侦测到连接断开比较麻烦，暂时先不做并发连接的统计
        # cls._sendStatsToConsoleUdp({'connNum':cls.connectionNumber})

    @classmethod
    def start(cls):
        """
        Run stats routine.
        """
        cls.clear()
        cls.runFlag = True  # 启动标识

        gevent.spawn(cls._independent_check)

                
    # 独立检查协程，检查上一秒统计数据是否发出了
    # 应该只对最后一秒有效，主统计协程里面发现到了新一秒会发送上一秒的统计
    @classmethod
    def _independent_check(cls):

        # 总是发送上一秒的统计，因为当前秒还没有结束，总计发送接收消息数量统计没有结束
        while True:

            if not cls.runFlag:
                break

            # check every 0.8 seconds
            time.sleep(0.4)

            curTime = getCurTime()

            # get last second to measure
            lastSecond = int(curTime) - 1

            cls._one_second_data_done_stats(lastSecond)


    @classmethod
    def stop(cls):
        """
        Stop stats routine.
        """
        # wait for more than 1 second, so stats greenlet could count last second
        time.sleep(1.2)
        cls.runFlag = False

    # 更新 以秒为单位的统计表
    @classmethod
    def _measure_per_second(cls, recTable, addAmount, curTime=None):
        
        if curTime is None:
            curTime = getCurTime()

        # get cur second to measure
        curSecond = int(curTime)
        # new second to stats
        if curSecond not in recTable:          
            recTable[curSecond] = addAmount
            # 新的一秒，看看前1秒统计有没有总结处理
            cls._one_second_data_done_stats(curSecond-1)
        # add one to  stats
        else:
            recTable[curSecond] += addAmount
        
        return curTime

    @classmethod
    def one_sent(cls):

        sentTime = cls._measure_per_second(cls.rpsTable,1)
        cls.totalSend +=1


        return sentTime


    @classmethod
    def connection_num_increace(cls):
        cls.connectionNumber +=1

    @classmethod
    def connection_num_decreace(cls):
        cls.connectionNumber -=1


        
    @classmethod
    def one_recv(cls,sentTime):
                
        recvTime = cls._measure_per_second(cls.tpsTable,1)
        cls.totalRecv +=1

        duration = recvTime - sentTime
        cls._measure_per_second(cls.responseTimeTable,duration,recvTime)

        
        if duration < 0.1 :
            cls.resptimeRange['<100ms'] += 1
        elif 0.1<= duration < 0.5 :
            cls.resptimeRange['100-500ms'] += 1
        elif 0.5<= duration < 1 :
            cls.resptimeRange['500-1000ms'] += 1
        elif 1<= duration < 3 :
            cls.resptimeRange['1000-3000ms'] += 1
        else :
            cls.resptimeRange['>=3000ms'] += 1

        return recvTime

    @classmethod
    def one_timeout(cls):

        cls._measure_per_second(cls.timeoutTable, 1)
        cls.totalTimeout += 1

        return


    @classmethod
    def one_error(cls, log_info: Union[None,str] = None):
        """
        Add one error to the statistics result, and write the error info to log file if needed.

        Parameters
        ----------
        log_info : Union[None,str], optional
            (Optional) the error info to be written to log file.
        """

        cls._measure_per_second(cls.errorTable, 1)
        cls.totalError += 1

        if log_info:
            TestLogger.write(log_info)
        return

Stats.clear()