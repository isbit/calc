# 
- Det skal lages en statistisk side. Med spøreundesøkelse og plottes representasjoner av undersøkelsene.
- Admin skal kunne opprette undersøkelser.
- Brukere skal kunne finne undersøkelser i en list, og besvare.
- AJAX og templates.

# Pseudokode:
          
- FUNKSJON. Opprette undersøkelse i form av tabell.
    - Registrere spørsmål og svaralternativer.    
    - Undersøkelse legges til i listen over tilgjengelige undersøkelser, questionnaires.
    - Spørsmål skal legges til i tabell: questionnaire
    - lage hashpassword på user_id, for anonymisering av brukeren?
    - Automatisk lagring av spørsmålene underveis

- FUNKSJON. Vise undersøkelser, i liste man kan velge undesøkelsen man svarer

- FUNKSJON. Vise undersøkelsen man har valgt.
    - Ta imot svarene.

- FUNKSJON. Besvarelse av undersøkelse.
    - Registrere valgte svar inn i en tabell.
    - Automatisk lagring av spørsmålene underveis

- FUNKSJON. Sortert visning av spørreundersøkelsene.

- FUNKSJON. Update/delete
    - Bruker endrer/sletter sine svar 
    - Admmin endrer/sletter brukere, tabeller osv

- FUNKSJON. Login
    
- FUNKSJON. Bruker
    - Preferanser til bruker (cookies/tables)

- FUNKSJON. Error display fra/i base.html

- AJAX
    - Klikke undersøkelse, viser undersøkelsen async.

- CSS
    - Flex
    - Absolute position
    - Fluid layout, forandre seg etter skjermstørrelse osv.
    - Phone layout

- HTML
    - Semantics tag

# Valgfrie oppgaver

- FUNKSJON. Bearbeide data. Backend?

- FUNKSJON. Plotte data.

- FUNKSJON. Premier for svar. Memory game med tilfeldige valgte. JS frontend?

- FUNKSJON. Search, med live display om ønskelig.

- FUNKSJON. Funksjonalitet, accesability. 

# Huskeliste

- Validering
    - JS og serversiden
    - Meaningfull errors should be dispalyed.
    - Alle funksjone.
    - Code seperation.


### Layout

You should use semantic HTML tags.
Use tags where it everywhere it makes sense.

- Some elements should be displayed using a flexbox.
- Some elements should use absolute positioning.
- The layout of your page should be fluid, i.e. adjust to different browser window sizes.
- For full points, you page needs to both look like it makes good use of a desktop screen, e.g. `>1200px`, but also be able to adjust to phone size, e.g. `375px`.

# Spørsmål til Leander
- Rest API.
- Data stored vs example data.
- Fluid layout vs phone layout.
- JS form validation vs server side validation.
- Authentication vs access control.
- Extensive API
- External API
- Prentasjonen? Hver for oss eller sammen?
- Every group should meet at least once with me, before handing in your draft report??

