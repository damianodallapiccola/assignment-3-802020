## How to run


Requirements:

- RabbitMq version: 3.7.18

- Python version: 3.7

- Flink version: 1.9.1

- Java version: 8+

- Maven


From the folder wher Flink is installed
 * if you want to change the number of Task Managers add them here `libexec/config/slaves`
 * if you want to change the number of tasks for each Task Manager modify this file: `libexec/config/flink-conf.yaml` (see picture below)

![](config.png)

start the cluster
 ```console
 libexec/bin/start-cluster.sh
 ```



From the root folder of the project:
 -run:
 ```console
 pip install requirements.txt
 ```

From `assignment-3-802020/code/customerstreamapp` execute this to run your Flink app:

 ```console
 mvn clean install
flink run target/customerstreamapp-0.1-SNAPSHOT.jar
 ```

From `assignment-3-802020/code/scripts` run 
 ```console
 python3 analytics_receiver.py
 ```
to run the analytics receiver


From `assignment-3-802020/code/scripts` run 
 ```console
python3 stream_sender.py <path_to_the_dataset>
 ```
to run the stream sender