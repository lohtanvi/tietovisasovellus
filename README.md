Tietovisasovellus (toteutus käynnissä - draft versio)

Sovelluksen avulla voidaan järjestää tietovisa -kyselyitä, joissa on kysymyksiä ja automaattisesti tarkastettavia vastauksia. Jokainen käyttäjä on tietovisan luoja tai tietovisan osallistuja.

Sovelluksen ominaisuuksia:
Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. (toteutus kesken - tietoturva ym. tarkistuksia ei ole toteutettu)
Osallistuja näkee listan tietovisa -kyselyistä ja voi liittyä tietovisaan. (toteutus kesken - roolin tunnista ei ole toteutettu, tietovisaan ei vielä mahdollista osallistua)
Osallistuja voi lukea tietovisan tekstimateriaalia sekä vastata tietovisa -kyselyn kysymyksiin. Tietovisasta saa pisteitä oikeiden vastausten perusteella. (ei toteutettu)
Osallistuja pystyy näkemään tilaston, mihin tietovisa- kyselyyn hän on osallistunut ja kuinka paljon hän on saanut kyseisestä tietovisasta pisteitä. (kesken - pohja luotu)
Luoja pystyy luomaan uuden tietovisa -kyselyn, muuttamaan olemassa olevan tietovisa -kyselyn kysymyksiä ja poistamaan tietovisa -kyselyn. Yhdessä tietovisassa on esimerkiksi 10 kysymystä, joista maksimissaan voi saada yhteensä 10 pistettä, yksi piste per oikea vastaus. (kesken - tietovisa poisto tai muuttaminen ei ole mahdollista)
Luoja pystyy lisäämään tietovisaan tekstimateriaalia ja tietovisakysymyksiä. Kysymyksien vastaukset voivat olla moni valinta -vaihtoehtoja tai tekstikenttä, johon tulee kirjoittaa kysymyksen oikea vastaus. (kesken - luoja pystyy luomaan kysymyksen ja antamaan vastauksen)
Luoja pystyy näkemään tilaston, keitä osallistujia on tietovisa -kyselyllä ja kuinka paljon osallistuja on tietovisa -kyselystä saanut. (ei toteutettu)

Sovellus on luotu Ubuntu 22.04.4 LTS versiolla.

Sovellus on testattavissa omalla koneella paikallisesti kurssimateriaalista löytyvän ohjeistuksen mukaisesti:

https://hy-tsoha.github.io/materiaali/aikataulu/#huomio-flyiosta
https://hy-tsoha.github.io/materiaali/osa-3/#versionhallinta


Sovelluksesta on testattavissa käyttäjätunnuksen luonti, tietovisan luominen ja kysymysten sekä vastausten luominen, osallistujan listaus tietovisoista. Sivuilta toiselle siirtyminen. 
Testauksessa huomattava, että tietovisan id on asetettu koodiin (quiz_id = 7) sekä tietovisan luojan id (creator_id = 2). 
