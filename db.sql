create DATABASE leave_management;

use leave_management;

CREATE TABLE leaves (
	ref_number int AUTO_INCREMENT PRIMARY KEY,
    leave_type varchar(255),
    from_date date,
    to_date date,
    create_timestamp timestamp
);