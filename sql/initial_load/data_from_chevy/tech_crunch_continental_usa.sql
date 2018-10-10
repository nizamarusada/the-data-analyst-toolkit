--drop table tech_crunch_continental_usa;

create
	table
		tech_crunch_continental_usa (
		permalink varchar(255),
		company varchar(255),
		num_employee varchar(255),
		category varchar(255),
		city varchar(255),
		state varchar(255),
		funded_date varchar(255),
		raised_amount varchar(255),
		raised_currency varchar(255),
		round varchar(255) );
		
select * from tech_crunch_continental_usa;
select count(*) from tech_crunch_continental_usa;