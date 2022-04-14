# 5GSMARTG_PYTHON
<br>
<h3>Questo programma è un software gratuito: puoi ridistribuirlo e/o modificarlo secondo i termini della GNU General Public License pubblicata da Free Software Foundation, versione 3 della Licenza, oppure qualsiasi versione successiva.<br>
<br>
Questo programma è distribuito nella speranza che possa essere utile, ma SENZA ALCUNA GARANZIA; senza nemmeno la garanzia implicita di COMMERCIABILITÀ o IDONEITÀ PER UNO SCOPO PARTICOLARE. Vedi il GNU General Public License per maggiori dettagli.<br>
<br>
<a href="http://www.gnu.org/licenses">GNU General Public License</a>
</h3>
<br>
<br><br>
Il software è diviso in 2 cartelle:<br>
<ul>
  <li>Publisher</li>
  <li>Subscriber</li>
</ul> 
<br>
<br>	
Il Publisher è stato sviluppato per interfacciarsi con il singolo nodo IoT ed inviare i campioni accellerometrici (x,y,z) verso il broker MQTT.<br>
<br>
Il Subscriber ha il compito inverso: recupera i campioni accellerometrici dal broker. Dal momento che ci sono (o ci saranno) più nodi IoT disponibili, nel Subscriber bisogna selezionare il nodo di interesse.
Al solo scopo di debug, all'interno del Subscriber è stato implementata una semplice e basilare interfaccia grafica che permette la selezione del nodo e la scelta di alcuni parametri relativi al processing.<br>
<br>
Aggiornamenti in fase di scrittura...
