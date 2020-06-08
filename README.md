# World-Cities-Data-Pickup

### What This Project Needs (This has to be installed)
* [lxml](https://lxml.de/)

---

### What there is still to be done
- [ ] use simple "==" instead of array.find
- [ ] refactor most of the if-statements (there are some that are not needed anymore)
- [x] there are cities that have only have of their name as a link and because of that the name gets split and we can't find the page for it - searching with next element in array to combat this, I fixed this by using hrefs that are on the site instead of names
- [ ] split main functions into smaller ones
- [ ] make it as fast as it can be
- [ ] start using try...except blocks
- [x] better image capturing
- [x] there are countries like - Japonia - which have different places to store theirs cities names - better city name capturing
- [ ] Białoruś isn't working like it should - better city name capturing
- [ ] there's a bug with "Położenie" in Tokio - it doesn't get the "Brak danych" mark
- [ ] in Miasta_w_Japonii it doesn't catch the Tokio - because it is in li/i/a not li/a
- [ ] get this code mostly working with around 10 countries (Then I'm satisfied)
- [ ] try using better data capturing - instead of making one big array maybe try getting the data just from the places that you need them (It could help with speed and the if statements)
- [ ] clean up "loops-for-cleaning"
- [ ] "liczba_ludności" and "gęstość" are usually with each other and not with their numbers