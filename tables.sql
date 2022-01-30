create database hotel;

use hotel;

create table room(
room_id  varchar(4) primary key NOT NULL, 
price  decimal(8, 2), 
room_type ENUM('舒适单人房','舒适双人房','豪华单人房','豪华双人房','行政套房'));


create table employee(
e_id varchar(8) primary key NOT NULL, 
full_name varchar(20),  
age INT, 
sex ENUM('男', '女') default '男', 
phone varchar(11), 
address varchar(100));

create table order_list(
order_no char(10) primary key unique, 
id char(18), 
room_id varchar(4), 
price decimal(8, 2), 
discount float, 
num_customers INT, 
dealer_id varchar(8), 
start_date varchar(20), -- 预计入住的date
end_date varchar(20),

order_date varchar(20), -- order的date
cur_time varchar(20), 
order_status ENUM('已完成', '入住中', '预订中'),
order_type ENUM('团体', '个人') default '个人',
foreign key(room_id) references room(room_id), 
foreign key(dealer_id) references employee(e_id));

create table check_in(
order_no char(10) NOT NULL, 
room_id varchar(10),
id char(18) NOT NULL, 
customer_name varchar(20), 
phone char(11),  
cur_date varchar(20), 
cur_time varchar(20), 
primary key(order_no, id),
foreign key(order_no) references order_list(order_no),
foreign key(room_id) references room(room_id));

create table VIP(
id char(18) primary key NOT NULL, 
customer_name varchar(20), 
sex ENUM('男', '女') default '男',
phone char(11),  
cur_level INT default 1, 
discount float, 
integration INT default 10);
