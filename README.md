# 5GSMARTG_PYTHON

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
Al solo scopo di debug, all'interno del Subscriber è stato implementata una semplice e basilare interfaccia grafica che permette la selezione del nodo e la scelta di alcuni parametri relativi al processing.
