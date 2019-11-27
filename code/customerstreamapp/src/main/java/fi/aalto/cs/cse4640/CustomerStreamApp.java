package fi.aalto.cs.cse4640;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSink;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSource;
import org.apache.flink.streaming.connectors.rabbitmq.common.RMQConnectionConfig;
import org.apache.flink.util.Collector;

import java.io.StringReader;
import java.text.SimpleDateFormat;
import java.util.Date;




public class CustomerStreamApp {

    public static void main(String[] args) throws Exception {
        //using flink ParameterTool to parse input parameters
        // final String input_rabbitMQ;
        final String input_rabbitMQ = "amqp://guest:guest@localhost:5672/";
        final String inputQueue = "data_streaming";
        // the following is for setting up the execution getExecutionEnvironment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        SimpleStringSchema inputSchema =new SimpleStringSchema();

        //checkpoint can be used for  different levels of message guarantees
        // select one of the following modes
        //final CheckpointingMode checkpointingMode = CheckpointingMode.EXACTLY_ONCE ;
        final CheckpointingMode checkpointingMode = CheckpointingMode.AT_LEAST_ONCE;
        env.enableCheckpointing(1000*60, checkpointingMode);
        // define the event time
        env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);
        //env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
        //if using EventTime, then we need to assignTimestampsAndWatermarks
        //now start with the source of data



        final RMQConnectionConfig connectionConfig = new 	RMQConnectionConfig.Builder()
                .setHost("localhost")
                .setPort(5672)
                .setUserName("guest")
                .setPassword("guest")
                .setVirtualHost("/")
                //.setUri(input_rabbitMQ)
                .build();

        RMQSource<String> btsdatasource= new RMQSource(
                connectionConfig,            // config for the RabbitMQ connection
                inputQueue,                 // name of the RabbitMQ queue to consume
                false,       // no correlation between event
                inputSchema);

        final DataStream<String> btsdatastream = env
                .addSource(btsdatasource)   // deserialization schema for input
                .setParallelism(1);

        btsdatastream.print();

        env.execute("Simple CS-E4640 BTS Flink Application");

    }

}

