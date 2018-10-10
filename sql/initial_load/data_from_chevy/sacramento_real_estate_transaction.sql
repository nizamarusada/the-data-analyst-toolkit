--drop table sacramento_real_estate_transaction;

create
	table
		sacramento_real_estate_transaction (
		street varchar(255),
		city varchar(255),
		zip varchar(255),
		state varchar(255),
		beds varchar(255),
		bath varchar(255),
		square_feet varchar(255),
		type varchar(255),
		sale_date varchar(255),
		price varchar(255),
		latitude varchar(255),
		longtiude varchar(255) );


--select * from sacramento_real_estate_transaction;
--select count(*) from sacramento_real_estate_transaction;
