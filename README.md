#Web store build using Django and docker

## Install and setup 

It works with different data base, default: SQLLite, can be changed in 
```
./ShoppingCart/ShoppingCart/settings.py
```
To format db use comand:
```
python ./ShoppingCart/manage.py migrate
```
To run:
```
python ./ShoppingCart/manage.py runserver
```
Also can be: (X.X.X.X - IP-adress, YYYY - port)
```
python ./ShoppingCart/manage.py runserver X.X.X.X:YYYY
```

## Docker

You can build docker image by using Dockerfile:
```
docker build -t image_name .
```
and run container with:
```
docker run -d -p container_port:outer_port image_name
```

## Auth

You can create user on the website, by manage.py file and directly in db

Creating superuser shoud do unly by manage.py:
```
python ./ShoppingCart/manage.py createsupperuser
```
With superuser account you have access to admin panel:

![Screenshot from 2022-12-03 17-11-02](https://user-images.githubusercontent.com/44704482/205447814-8039027c-91e6-4ff1-a235-adaf8b4c299f.png)

## Demo

/login
![Screenshot from 2022-12-03 17-16-00](https://user-images.githubusercontent.com/44704482/205448086-150f4789-6fb6-49dd-bb6f-c413c26e155c.png)

/signup
![Screenshot from 2022-12-03 17-16-19](https://user-images.githubusercontent.com/44704482/205448147-5d142886-20d2-4a9c-a951-31c1b4740300.png)
/items
![Screenshot from 2022-12-03 17-17-38](https://user-images.githubusercontent.com/44704482/205448224-caf9a83b-f3d8-4c17-bcd7-90a20b05172c.png)

/cart

![Screenshot from 2022-12-03 17-18-45](https://user-images.githubusercontent.com/44704482/205448270-4a425d0c-5606-4bcf-9ac4-0443b493885e.png)

