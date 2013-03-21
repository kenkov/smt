build :
	python jec_createdb.py
	python jec_createngramdb.py

db :
	python jec_createdb.py

ngram : db
	python jec_createngramdb.py

.PHONY : clean
clean :
	rm :test:
