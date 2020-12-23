This is a simple phonebook app which was created to demonstrate skills in OO design as well as knowledge and use cases of various design patterns.

**CLI Examples**

```./bin/phonebook_cli-q```                                                                          returns all records in database<br>
```./bin/phonebook_cli -q -n Richard```                                                               returns all records in which name field contains Richard<br>
```./bin/phonebook_cli -q -n en -p 647 -adr Street```                                                 returns all records in which name contains en, phone contains 647, address contains Street<br>
```./bin/phonebook_cli -a -n John Doe -p 647 555 1234 -adr 1234 Test Street```                        add record with provided values<br>
```./bin/phonebook_cli -d -n John Doe```                                                              delete all records which name contains "John Doe"<br>
```./bin/phonebook_cli -u -n John Doe -un John Doe -up 647 112 4456 -uadr 1234 Test Street```         update record with name John Doe and set to provided values (flags starting with -u )<br>
```./bin/phonebook_cli -au 3```                                                                       change the write rules to allow only record with unique phone numbers (see -h for full list)<br>
```./bin/phonebook_cli -s csv```                                                                      change the serial format for exports to csv format (see -h for full list)<br>
```./bin/phonebook_cli -e default```                                                                  export all data from database to default data directory (set in lib.api.conf.AppConfig)<br>
```./bin/phonebook_cli -e /mnt/users/jacob/dev/phonebook/data/exported_data```                        export all data to custom directory<br>
```./bin/phonebook_cli -au 2 -a -n John Doe -p 647 222 2122 -adr 144 Test St -s html -e default```    change write auth rule to write on unique names, add a new user, change the serial format to html, export to the deafult export filepath<br>


**Run All Tests**
```python -m unittest discover -s ./test -t ./test```