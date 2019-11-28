package fi.aalto.cs.cse4640;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.api.java.tuple.Tuple;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.api.java.tuple.Tuple6;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.core.fs.FileSystem;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.timestamps.AscendingTimestampExtractor;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSink;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSource;
import org.apache.flink.streaming.connectors.rabbitmq.common.RMQConnectionConfig;
import org.apache.flink.util.Collector;

import java.io.StringReader;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;


public class CustomerStreamApp {

    public static void main(String[] args) throws Exception {

        //using flink ParameterTool to parse input parameters
        // final String input_rabbitMQ;
        final String input_rabbitMQ = "amqp://guest:guest@localhost:5672/";
        final String inputQueue = "data_streaming";
        final String outputQueue = "analytics_streaming";
        // the following is for setting up the execution getExecutionEnvironment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        SimpleStringSchema inputSchema =new SimpleStringSchema();

        //checkpoint can be used for  different levels of message guarantees
        // select one of the following modes
        //final CheckpointingMode checkpointingMode = CheckpointingMode.EXACTLY_ONCE ;
        final CheckpointingMode checkpointingMode = CheckpointingMode.AT_LEAST_ONCE;
        //env.enableCheckpointing(1000*60, checkpointingMode);
        // define the event time
        //env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);
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

        RMQSource<String> datasource= new RMQSource(
                connectionConfig,            // config for the RabbitMQ connection
                inputQueue,                 // name of the RabbitMQ queue to consume
                false,       // no correlation between event
                inputSchema);


        final DataStream<String> datastream = env
                .addSource(datasource)   // deserialization schema for input
                .setParallelism(1);



        // datastream.print();

        // INPUT
        //         0                   1               2             3             4             5
        //tpep_pickup_datetime, passenger_count, trip_distance, PULocationID, DOLocationID, total_amount

        // OUTPUT
        //     0                1                 2                3                4              5
        //PULocationID, initial_timestamp, final_timestamp, total_passengers, total_distance, total_amount


        env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);

        SingleOutputStreamOperator<Tuple6<Integer, Integer, Float, Integer, Integer, Float>> mapString = datastream.map(new MapFunction<String, Tuple6<Integer, Integer, Float, Integer, Integer, Float>>() {
            @Override
            public Tuple6<Integer, Integer, Float, Integer, Integer, Float> map(String s) {

                String[] fieldArray = s.split(",");
                Tuple6<Integer, Integer, Float, Integer, Integer, Float> out = new
                        Tuple6<>(Integer.parseInt(fieldArray[0]), Integer.parseInt(fieldArray[1]), Float.parseFloat(fieldArray[2]), Integer.parseInt(fieldArray[3]),
                        Integer.parseInt(fieldArray[4]),  Float.parseFloat(fieldArray[5]));
                return out;
            }
        });

        SingleOutputStreamOperator<String> keyedStream = mapString.assignTimestampsAndWatermarks(new AscendingTimestampExtractor<Tuple6<Integer, Integer, Float, Integer, Integer, Float>>() {
            @Override
            public long extractAscendingTimestamp(Tuple6<Integer, Integer, Float, Integer, Integer, Float> element) {
                return element.f0 * 1000;
            }
        }).keyBy(3)
        .window(TumblingEventTimeWindows.of(Time.hours(1)))
                .apply(new WindowFunction<Tuple6<Integer, Integer, Float, Integer, Integer, Float>, String, Tuple, TimeWindow>() {
                    @Override
                    public void apply(Tuple tuple, TimeWindow timeWindow, Iterable<Tuple6<Integer, Integer, Float, Integer, Integer, Float>> iterable, Collector<String> collector) throws Exception {

                        // INPUT
                        //         0                   1               2             3             4             5
                        //tpep_pickup_datetime, passenger_count, trip_distance, PULocationID, DOLocationID, total_amount

                        // OUTPUT
                        //     0                1                 2                3                4              5
                        //PULocationID, initial_timestamp, final_timestamp, total_passengers, total_distance, total_amount

                        Iterator<Tuple6<Integer, Integer, Float, Integer, Integer, Float>> iterator = iterable.iterator();
                        Tuple6<Integer, Integer, Float, Integer, Integer, Float> init = iterator.next();

                        int PULocationID = init.f3;
                        int initial_timestamp = init.f0;
                        int final_timestamp = init.f0;
                        int total_passengers = 0;
                        float total_distance = 0;
                        float total_amount = 0;

                        // System.out.println("apply");

                        for (Tuple6<Integer, Integer, Float, Integer, Integer, Float> next : iterable) {

                            if (next.f0 < initial_timestamp) {
                                initial_timestamp = next.f0;
                            }
                            if (next.f0 > final_timestamp) {
                                final_timestamp = next.f0;
                            }
                            total_passengers = total_passengers + next.f1;
                            total_distance = total_distance + next.f2;
                            total_amount = total_amount + next.f5;
                        }

                        collector.collect("{\"PULocationID\":"+ Integer.toString(PULocationID) +
                                ", \"initial_timestamp\":" + Integer.toString(initial_timestamp)+
                                ", \"final_timestamp\":" + Integer.toString(final_timestamp) +
                                ", \"total_passengers\":" + Integer.toString(total_passengers) +
                                ", \"total_distance\":" + Float.toString(total_distance) +
                                ", \"total_amount\":" + Float.toString(total_amount) +
                                "}");
                    }

        });

        // keyedStream.writeAsText("/outFilePath/" + "/avgspeedfines.csv", FileSystem.WriteMode.OVERWRITE).setParallelism(1);


        //send the alerts to another channel
        RMQSink<String> sink =new RMQSink<String>(
                connectionConfig,
                outputQueue,
                new SimpleStringSchema());

        keyedStream.addSink(sink);
        //use 1 thread to print out the result
        // keyedStream.print().setParallelism(1);








        env.execute("Simple CS-E4640 BTS Flink Application");


    }

    public static class EventParser implements FlatMapFunction<String, StreamingEvent> {

        @Override
        public void flatMap(String line, Collector<StreamingEvent> out) throws Exception {
            CSVRecord record = CSVFormat.RFC4180.withIgnoreHeaderCase().parse(new StringReader(line)).getRecords().get(0);
            //just for debug
            System.out.println("Input: " + line);




            //filter all records with isActive =false
            /*if (Boolean.valueOf(record.get(6))) {
                SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss z");
                Date date = format.parse(record.get(3));
                BTSAlarmEvent alarm = new BTSAlarmEvent(record.get(0), record.get(1), record.get(2), date, Float.valueOf(record.get(4)), Float.valueOf(record.get(5)));
                out.collect(alarm);


           }*/
        }
    }

}

