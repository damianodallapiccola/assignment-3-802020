
# Assignment 3 802020  
  
For this assignment I used Python, RabbitMQ, NiFi and Mongodb. The datasets I chose are the [Indoor Localization Dataset](https://zenodo.org/record/2671590#.XXJahPxRUlU) for client1 and a version mobified by me of [Films Dataset](https://perso.telecom-paristech.fr/eagan/class/igr204/datasets) for client2.  
  
  
---  
## Part 1 - Design for streaming analytics  
  
**1)** Select a dataset suitable for streaming analytics for a customer as a running example (thus the basic unit of the data should be a discrete record/event data). Explain the dataset and at least two different analytics for the customer: (i) a streaming analytics which analyzes streaming data from the customer (customerstreamapp) and (ii) a batch analytics which analyzes historical results outputted by the streaming analytics. The explanation should be at a high level to allow us to understand the data and possible analytics so that, later on, you can implement and use them in answering other questions.
  
The chosen dataset is a modified version of the Yellow Taxi Trip Records.
I removed some columns and I keept only 700k lines for testing purposes ([dataset_v1](https://drive.google.com/file/d/1gla8axt2vr7OoQ85O5UXhkbtZk--LYit/view?usp=sharing)). Then, using a script, I changed all the dates&time data into timestamps (seconds elapsed from 1/1/1970) and I also removed the header to simplify the process ([dataset_v2](https://drive.google.com/file/d/1Im7cRDH6_i319aKNjukBjnL3-ZZ-7hxU/view?usp=sharing)). I used this final dataset as collection of events for the stream.

An event is defined as:
 * tpep_pickup_datetime (int): date and time of the clients pickup (expressed in number of seconds elapsed from 1/1/1970).
 * passenger_count (int): the number of passengers in the vehicle
 * trip_distance (float): elapsed trip distance in miles
 * PULocationID (int): city zone of the pickup
 * DOLocationID (int): city zone of the destination
 * amount (float): amount charged to passengers
  
Client: Uber-like company
Data: Every event is created and sent automatically when a client books a ride (specifying pickup place, destination and number of passengers). trip_distance, PULocationID, DOLocationID and total_amount are automatically calculated.




i) streaming analytics: the client wants to have real-time data (every hour) related to the most profitable area of the city, to be able to move his drivers in that specific area, to increase the possibility of finding clients.

Result of the analytics:
 * PULocationID (int): city zone of the pickup
 * initial_timestamp (int): timestamp of the first event recorded in the window of one hour (expressed in number of seconds elapsed from 1/1/1970)
 * final_timestamp (float): timestamp of the last event recorded in the window of one hour (expressed in number of seconds elapsed from 1/1/1970).
 * total_passengers (int): total number of passenger during all the travels
 * total_distance (int): total distance traveled by the driver
 * total_amount (float): total amount charged to all the clients

ii) batch analytics: every 24 hours the system returns a statistic about the most profitable zones, the most profitable hours, the most profitable days, ...
These anaysis could help to reorganize the distribution of drivers in the city and also the quantity needed during the different hours and days.

It's also possible to train, once a week or month, a machine learning model on the data to make some predictions (I will explain later all the tecnologies used for the implementation).


**2)** Customers will send data through message brokers/messaging systems which become data stream sources. Discuss and explain the following aspects for the streaming analytics: (i) should the analytics handle keyed or non-keyed data streams for the customer data, and (ii) which types of delivery guarantees should be suitable.  

  i) the analytics will handle keyed data streams (keyed by the zone of the pickup, **PULocationID**), allowing also a parallel analysis of the data, since the processing of each data related to a different **PULocationID** is indipendent.
  
  ii) I will implement at-most-once delivery guarantee because in our case we can accept data losses and we will have also better performances (less resource usage for handle duplicated messagges). Exactly-once delivery guarantee is of course suitable but, since is not strictly necessary, I decided to not implement it to reduce the complexity  and the resources needed.
  
**3)** Given streaming data from the customer (selected before). Explain the following issues:(i) which types of time should be associated with stream sources for the analytics and be considered in stream processing (if the data sources have no timestamps associated with events, then what would be your solution), and (ii) which types of windows should be developed for the analytics (if no window, then why). Explain these aspects and give examples.   
  
  The dataset chosen has a field called **tpep_pickup_datetime** that represent the timestamp expressed in number of seconds elapsed from 1/1/1970. Since I am going to use a tumbling window of one hour to analyze the streaming, the timestamp is going to be used as the main time for the analysis (the stream is going to be based on the event-time, not on the processing-time).
  
  For example, my first window will contain all the events (related only to one **PULocationID**) between the first one and the last event with a timestep less or equal to the timestep of the first event plus one hour.
  
  
  
**4)**  Explain which performance metrics would be important for the streaming analytics for your customer cases.
 * throughput
 * Loss rate
  
**5)**  Provide a design of your architecture for the streaming analytics service in which you clarify: customer data sources, mysimbdp message brokers, mysimbdp streaming computing service, customer streaming analytics app, mysimbdp-coredms, and other components, if needed. Explain your choices of technologies for implementing your design and reusability of existing assignment works. Note that the result from customerstreamapp will be sent back to the customer in near real-time.
  
  
  
  In the picture is shown the architecture of the system developed. For semplicity is shown only one customer, but this platform can handle multiple customer. Each customer will have his's own *stream_sender*(simulation of the data coming from every booking) and *analytics_receiver*(receiver of the real-time analysis), two rabbitMQ queue to send and receive data from the analytics and a personalized Flink app to handle his data. The database for the storage will be the same. 
  
  * **customer data sources**: the data are coming from 
  
  
  * **mysimbdp message brokers**: 
  
  
  * **mysimbdp streaming computing service**:
    
  
  * **customer streaming analytics app**:
  
  * **mysimbdp-coredms**:
  
  /usr/local/Cellar/apache-flink/1.9.1/libexec/bin/start-cluster.sh
  
---  
## Part 2 - Implementation of streaming analytics
  
**1)** Explain the implemented structures of the input streaming data and the output result, and the data serialization/deserialization, for the streaming analytics application (customerstreamapp) for customers.



**2)** Explainthekeylogicoffunctionsforprocessingevents/recordsincustomerstreamappin your implementation.



**3)**  Run customer streamapp and show the operation of the customer streamapp with your test environments. Explain the test environments. Discuss the analytics and its performance observations.



**4)** Present your tests and explain them for the situation in which wrong data is sent from or is within data sources. Report how your implementation deals with that (e.g., exceptions, failures, and decreasing performance). You should test with different error rates.



**5)** Explain parallelism settings in your implementation and test with different (higher) degrees of parallelism. Report the performance and issues you have observed in your testing environments.



## Part 3 - Connection


**1)**  If you would like the analytics results to be stored also into mysimbdp-coredms as the final sink, how would you modify the design and implement this (better to use a figure to explain your design).
    
    
**2)**  Given the output of streaming analytics storedinmysimbdp-coredmsforalongtime. Explain a batch analytics (see also Part 1, question 1) that could be used to analyze such historical data. How would you implement it?
    
    
**3)**   Assume that the streaming analytics detects a critical condition (e.g., a very high rate of alerts) that should trigger the execution of a batch analytics to analyze historical data. How would you extend your architecture in Part 1 to support this (use a figure to explain your work)?.
    
    
**4)**  If you want to scale your streaming analytics service for many customers and data, which components would you focus and which techniques you want to use?
    
    
**5)**  Is it possible to achieve end-to-end exactly once delivery in your current implementation? If yes, explain why. If not, what could be conditions and changes to make it happen? If it is impossible to have end-to-end exactly once delivery in your view, explain why.

