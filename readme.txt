This application selects 2.69 % of (not logged in users) traffic and tracks their actions.
We can trigger exit-intent event and save actions the user took.
We can predict time of leaving, trigger an event ( show ads or whatever ) and record users actions.

Our application functional requirements:
1. selects 2.69 % of traffic.
2. trigger exit intent event ( when mouse leaves the browser from the top ).
3. predict session length and trigger an event if the user is predicted to leave.
2. save this groups every action ( page load, exit intent and page unload ( user leaving )) actions to redis database.

Non functional requirements:
1. this works in chrome and safari and mozilla
2. this works in desktop not mobile
3. redis data automatically saves to the host machine.


Still to do
1 todo:  visualize all of the collected data.

