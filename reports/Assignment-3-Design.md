
# Assignment 3 802020  
  
For this assignment I used Python, RabbitMQ, NiFi and Mongodb. The datasets I chose are the [Indoor Localization Dataset](https://zenodo.org/record/2671590#.XXJahPxRUlU) for client1 and a version mobified by me of [Films Dataset](https://perso.telecom-paristech.fr/eagan/class/igr204/datasets) for client2.  
  
  
---  
## Part 1 - Design for streaming analytics  
  
**1)** Select a dataset suitable for streaming analytics for a customer as a running example (thus the basic unit of the data should be a discrete record/event data). Explain the dataset and at least two different analytics for the customer: (i) a streaming analytics which analyzes streaming data from the customer (customerstreamapp) and (ii) a batch analytics which analyzes historical results outputted by the streaming analytics. The explanation should be at a high level to allow us to understand the data and possible analytics so that, later on, you can implement and use them in answering other questions.  
  
  
  
**2)** Customers will send data through message brokers/messaging systems which become data stream sources. Discuss and explain the following aspects for the streaming analytics: (i) should the analytics handle keyed or non-keyed data streams for the customer data, and (ii) which types of delivery guarantees should be suitable.   
  
  
  
**3)** Given streaming data from the customer (selected before). Explain the following issues:(i) which types of time should be associated with stream sources for the analytics and be considered in stream processing (if the data sources have no timestamps associated with events, then what would be your solution), and (ii) which types of windows should be developed for the analytics (if no window, then why). Explain these aspects and give examples.   
  
  
  
**4)**  Explain which performance metrics would be important for the streaming analytics for your customer cases.
  
  
  
**5)**  Provide a design of your architecture for the streaming analytics service in which you clarify: customer data sources, mysimbdp message brokers, mysimbdp streaming computing service, customer streaming analytics app, mysimbdp-coredms, and other components, if needed. Explain your choices of technologies for implementing your design and reusability of existing assignment works. Note that the result from customerstreamapp will be sent back to the customer in near real-time.
  
  
  
  
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

