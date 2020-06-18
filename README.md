# World-Cities-Data-Pickup

### What This Project Needs (This has to be installed)
* [python](https://www.python.org/)
* [lxml](https://lxml.de/)

---

### What there is still to be done
- [ ] split main functions into smaller ones
- [ ] get this code mostly working with around 10 countries (Then I'm satisfied)
- [ ] Białoruś isn't working like it should - better city name capturing - cities names are in tables not lists
- [ ] in Miasta_w_Japonii it doesn't catch the Tokio - because it is in li/i/a not li/a
- [x] delete unused if-statements
- [x] clean up "loops-for-cleaning"
- [x] where possible use simple "==" instead of array.find function
- [x] restrict making http requests to as few as possible
- [x] try using better data capturing - instead of making one big array maybe try getting the data just from the places that you need them (It could help with speed and the if statements)
- [x] there are cities that have only have of their name as a link and because of that the name gets split and we can't find the page for it - searching with next element in array to combat this, I fixed this by using hrefs that are on the site instead of names
- [x] start using try...except blocks
- [x] better image capturing
- [x] there are countries like - Japonia - which have different places to store theirs cities names - better city name capturing
- [x] there's a bug with "Położenie" in Tokio - it doesn't get the "Brak danych" mark
- [x] "liczba_ludności" and "gęstość" are usually with each other and not with their numbers
- [x] there are problem with "Burmistrz" there are sometimes random things after him, that don't get picked up in the same element
- [x] fuck meee. not every "Położenie" has just N, E, some are W, S - why did I forget this