# Lightweight Dispersy Example

This is a lightweight example project for those learning Dispersy (me).

Dispersy has changed alot in the past year, the tutorials no longer reflect state-of-the-art and they were hard (for me) to adapt to the latest version.

This example is pieced together by looking at communities in the Tribler source, unit tests, tutorials & papers available. 

I cannot guarantee this is how you should use Dispersy, merely how I figured out how to get it working. I may be incorrect in my understanding and comments. Nevertheless, I hope it helps someone else out there. 

I hope you enjoy this project and learning this fine message dissemination framework, Dispersy!

### Quickstart

git clone --recursive git@github.com:jarradh/DispersyExample.git dispersy_example
cd dispersy_example

Open 3 Shells and run in each;

./node1.sh  
./node2.sh  
./node3.sh

Over a small amount of time you will see each node Fully Distribute the messages sent to the community instance by the clients.

### How does it work?

Code is (crudely) commented.  
Start reading from src/main.py at EOF and follow code to learn.
