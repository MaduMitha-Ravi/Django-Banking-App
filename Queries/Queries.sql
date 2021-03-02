SELECT id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
	FROM public.auth_user;
	



-----------------------------------------------------------------
CREATE OR REPLACE FUNCTION insert_reguser_auth_user_func()
RETURNS trigger AS
$$
BEGIN
INSERT INTO public.auth_user(
	password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	VALUES (NEW.password, CURRENT_TIMESTAMP, false, NEW.username, NEW.firstname, NEW.lastname, NEW.email, false, true, CURRENT_TIMESTAMP);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

drop function insert_reguser_auth_user_func CASCADE;
--drop trigger insert_reguser_auth_user on public."Banker_registercustomers";

CREATE TRIGGER insert_reguser_auth_user
  AFTER INSERT
  ON public."Banker_registercustomers"
  FOR EACH ROW
EXECUTE PROCEDURE insert_reguser_auth_user_func();

-----------------------------------------------------------------


CREATE TRIGGER update_transactions_onstocks
  AFTER INSERT
  ON public."Customer_stocktrade"
  FOR EACH ROW
EXECUTE PROCEDURE update_transactions_onstocks_func();

drop function update_transactions_onstocks CASCADE

CREATE OR REPLACE FUNCTION update_transactions_onstocks_func()
RETURNS trigger AS
$$
BEGIN

#SET @account_id = (SELECT account_id FROM public."Banker_registercustomers" WHERE  )

IF NEW.stock_message = 'Stock Sold successfully' THEN


	INSERT INTO public."Customer_transactions"(
		transaction_amount_currency, transaction_amount, transaction_status, transaction_message, transaction_timestamp, transaction_type, account_id_id, id_id)
		VALUES ('CAD', NEW.stock_count * NEW.stock_price, 'Posted', 'Stock', CURRENT_TIMESTAMP, 'CREDIT', NEW.id_id, NEW.id_id);
	

	UPDATE public."Banker_registercustomers"
	SET depositamount = depositamount + (NEW.stock_count * NEW.stock_price)
	WHERE  = NEW.id_idaccount_id;                             
	

END IF;

IF NEW.stock_message = 'Stock bought successfully' THEN


	INSERT INTO public."Customer_transactions"(
		transaction_amount_currency, transaction_amount, transaction_status, transaction_message, transaction_timestamp, transaction_type, account_id_id, id_id)
		VALUES ('CAD', NEW.stock_count * NEW.stock_price, 'Posted', 'Stock', CURRENT_TIMESTAMP, 'DEBIT', NEW.id_id, NEW.id_id);
	

	UPDATE public."Banker_registercustomers"
	SET depositamount = depositamount - (NEW.stock_count * NEW.stock_price)
	WHERE account_id = NEW.id_id;                             
	

END IF;

RETURN NEW;

END;
$$
LANGUAGE 'plpgsql';


-----------------------------------------------------------------


