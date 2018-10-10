--drop table consumer_complaints;

create
	table
		consumer_complaints (
		date_received varchar(255),
		product_name varchar(255),
		sub_product varchar(255),
		issue varchar(255),
		sub_issue varchar(255),
		consumer_complaint text,
		company_public_response text,
		company varchar(255),
		state_name varchar(255),
		zip_code varchar(255),
		tags varchar(255),
		consumer_consent_provided varchar(255),
		submitted_via varchar(255),
		date_sent_to_company varchar(255),
		company_response_to_consumer varchar(255),
		timely_response varchar(255),
		consumer_disputed varchar(255),
		complaint_id varchar(255) );


--select * from consumer_complaints;
--select count(*) from consumer_complaints;
