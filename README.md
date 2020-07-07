# Drive-Through Restaurant P2P
This project is composed of several nodes, those entities are the _Restaurant_, _Clerk_, _Chef_ and _Waiter_. The nodes communicate between them in a ring mode to deal with the request and prepare the response. 
Each node has two queue structs, a entrance and an exit queue (__queuein__ and __queueout__), the node process the messages located in queuein and stores the responses in queueout.

The entities in the first moment, they only know the first node in the ring, after the exchange, some messages, the nodes the others address and set up the platform. The Client sends a request to the Restaurant that initiate a single flow of messages that runs across all entities. When a node receives a message, its checks if its responsibility, depending on the content of the message, the node will add it to its entrance queue. If the message flow is empty, the node inserts a message in the flow, or just pass it to the next node in the ring.

## Prerequisites

* Clone this repository

## How to run
Open two terminals:

simulation:
```console
$ python simulation.py
```

client:
```console
$ python client.py
```

## Git Upstream

Keep your fork sync with the upstream

```console
$ git remote add upstream git@github.com:mariolpantunes/load-balancer.git
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```

## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)
* **Camila Uachave** - [CamilaUachave](https://github.com/CamilaUachave)
* **Jean Brito** - [JeanBrito](https://github.com/JoelBrito13)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
