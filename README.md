Multi-master replication
-----
Implementation of Multi-master replication in a cluster of 2 instances.

## Getting Started

1.git clone https://github.com/gadavivi/multi-master-replication.git  
2.In the docker-compose file to the set the SECOND_MASTER to the other master   
3.install docker  
4.run:   
```
> cd multi-master-replication
> docker-compose up
```

## Design
The goal of this cluster is to sync one object's data between two machines

I choose to achieve this goal with a multi master architecture.  
it means that every node is acting as a master and each master is responsible to sync the other with the most  
relevant object.

## The flow

* 1.post request arrives to one of the master.  
* 2.this master change his object state and save the current timestamp.  
* 3.every master checks every second in a separate thread if his state has changed.  
   * 3.1 if yes, it send the change to the second master.
   * 3.2 if no, it sleep for 1 second.  
* 4.The "second" master check if a given timestamp from step 3 is newer then what he has.  
    * 4.1 if yes, it updates his state.  
    * 4.2 if no, it does't do anything.    
    * 4.3 there is a tie! in this case to break the tie, the data with the smaller lexicographic md5 order is taken.
    
## CAP Theory
This architecture choose to prefer Availability over Consistency - This system is eventual consistency, because the sync is done trough a thread that ran every one second.  

