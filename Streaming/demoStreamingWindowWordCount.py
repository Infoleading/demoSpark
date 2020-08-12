from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


if __name__ == '__main__':
    if len(sys.argv)!=3:
        print("Usage: WindowWordCount.py <hostname> <port>",file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName="StreamingWindowWordCount")
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint("file:///root/tmp")
    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    counts = lines.flatMap(lambda line: line.split(" "))\
        .map(lambda x:(x, 1))\
        .reduceByKeyAndWindow(lambda a,b:a+b, lambda a,b:a-b, 30, 10)
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()
