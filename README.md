# db_recordcompany

-Πατήστε Code->Download ZIP<br/>
-Αποσυμπιέστε το περιεχόμενο

1) Εγκαταστήστε την python:

link:https://www.python.org/downloads 
Κατεβάστε την έκδοση 3.8 ή πιο πρόσφατη, και εγκαταστήστε την στον υπολογιστή σας

2) Εγκαταστήστε τις βιβλιοθήκες pymysql και pillow:

Βρείτε που είναι εγκατεστημένες οι βιβλιοθήκες της Python. Ένας εύκολος τρόπος είναι να ανοίξετε το IDLE. Εκεί, πατήστε File->New File και
στο νέο παράθυρο πατήστε File->Save As. Πατήστε με διπλό κλικ στο κενό της μπάρας διεύθυνσης που σας δείχνει και αντιγράψτε την.

Στη συνέχεια, εκτελέστε το CMD.exe (μπορείτε να το βρείτε απο την γρήγορη αναζήτηση των Windows), πληκτρολογήστε "cd", αφήστε κενό, επικολλήστε τη διεύθυνση που βρήκατε πριν
και προσθέστε στο τέλος "\Scripts". Πατήστε enter. Έπειτα, πληκτρολογήστε "pip install PyMySQL" και πατήστε enter. Αφού ολοκληρωθεί η εγκατάσταση, πληκτρολογήστε
"pip install Pillow"  και πατήστε enter.

3) Εγκαταστήστε το XAMPP:

Κατεβάστε το από τη διεύθυνση https://www.apachefriends.org/index.html και εγκαταστήστε το.

4) Εκτελέστε το XAMPP:

Εκτελέστε το xampp-control.exe. Στο παράθυρο που θα ανοίξει, πατήστε το κουμπί "Start" στα "Apache" και "MySQL"

5) Φόρτωση της βάσης δεδομένων:

Ανοίξτε έναν φυλλομετρητή, πληκτρολογήστε http://localhost/phpmyadmin και πατήστε enter.
Επιλέξτε την επιλογή New. Πληκτρολογήστε ως όνομα της βάσης δεδομένων το "recordcompany2",επιλέξτε το "utf8mb4_general_ci" και πατήστε create.
Επιλέξτε την "recordcompany2" και μετά επιλέξτε το "import".
Πατήστε "Επιλογή αρχείου", επιλέξτε το αρχείο "record_company.sql" και πατήστε "Go".

6) Εκτέλεση εφαρμογής:

Ανοίξτε το IDLE, πατήστε File->Open, επιλέξτε το αρχείο "main.py" και πατήστε άνοιγμα.(Σημείωση: Όλα τα αρχεία της εφαρμογής θα πρέπει να είναι στον ίδιο φάκελο)
Στο νέο παράθυρο που άνοιξε, πατήστε Run->Run Module.
Εάν δεν έχετε κάνει αλλαγές στο phpmyadmin, το όνομα χρήστη είναι root και τον κωδικό αφήστε τον κενό.

