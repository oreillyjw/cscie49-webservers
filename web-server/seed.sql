use cscie49_fp_product;

CREATE TABLE product (
    sku varchar(100),
    imageLocation varchar(250),
    title varchar(250)
);

INSERT INTO product (sku, imageLocation, title)
values("1234UK","https://images-na.ssl-images-amazon.com/images/I/51qlgJ6ZojL.jpg", "Harry Potter and the Sorcerer's Stone");

INSERT INTO product (sku, imageLocation, title)
values("23423WS","https://images-na.ssl-images-amazon.com/images/I/51FMxz1kEUL._SX317_BO1,204,203,200_.jpg", "Romeo and Juliet");
