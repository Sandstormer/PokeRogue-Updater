
headerNames = ['N°','Chrom.','Nom','Type','Talents','Capacités Œuf','Cout','Total','PV','Atq','Déf','ASp','DSp','Vit']
altText = ['Capacités','Principaux','Caché','Passif','Entrez','Puis.','Préc.','PP','Ajouter aux filtres','Champi Mémoriel',
           'Évolutions','Capacités Œuf','Rare Capac. Œuf','Commun','Super','Hyper','CT','N.','Évo','Œuf']
catToName = ['Type','Talent','Capacité','Gen','Cout','Sexe','Mode','Œuf','Variantes Chromatique','Biome','Lié à','Étiquette']
biomeText = ['Commun','Peu Commun','Rare','Super Rare','Hyper Rare','Boss','Com.','PC','Rare','SR','HR',
             'Aube','Jour','Crépuscule','Nuit']
infoText = ['Bonheur par Bonbon','Passif','Cout réduit','Acheter un Œuf','Talent Caché',
            'Exclusif à l’Œuf','Exclusif aux Bébés','Pokémon Paradoxe','Changement de forme','Biomes','Filtres']
# tagToDesc = [
#     "Cibles: Ennemi aléatoire",
#     "Cibles: Tous les ennemis",
#     "Cibles: Champ entier",
#     "Taux de critique élevé",
#     "Coup critique garanti",
#     "Taux critique de l'utilisateur +2",
#     "Attaque de l'utilisateur au max",
#     "Coûte 33% des PV",
#     "Coûte 50% des PV",
#     "Recul de 50% des PV",
#     "Recul de 50% des dégâts",
#     "Recul de 33% des dégâts",
#     "Recul de 25% des dégâts",
#     "30% d'infliger le double de dégâts",
#     "30% de voler l'objet le plus rare",
#     "Régénère 100% des dégâts infligés",
#     "Régénère 75% des dégâts infligés",
#     "Régénère 50% des dégâts infligés",
#     "Régénère selon l'Attaque de la cible",
#     "Soigne les altérations d'état",
#     "Soigne le Sommeil",
#     "Soigne la Gelure",
#     "Soigne la Brûlure",
#     "Aucun effet sur Plante/Envelocape",
#     "Ne peut pas ensemencer les types Plante",
#     "Déclenche le talent Secours",
#     "Déclenche le talent Danseur",
#     "Déclenche le talent Cavalier des Vents",
#     "Amplifié par Aiguisage",
#     "Amplifié par Poing de Fer",
#     "Amplifié par Méga Blaster",
#     "Amplifié par Mâchoire Forte",
#     "Amplifié par Téméraire",
#     "Aucun effet sur Pare-Balles",
#     "Empêché par le talent Moiteur",
#     "Attaque sonore",
#     "Ignore Clonage",
#     "Ignore les talents",
#     "Ignore Abri",
#     "L'utilisateur se retire",
#     "La cible se retire",
#     "Frappe 2 fois",
#     "Frappe 3 fois",
#     "Frappe 10 fois",
#     "Frappe 2 à 5 fois",
#     "Se répète pendant 2 à 3 tours",
#     "Retire les pièges",
#     "Piège et blesse la cible",
#     "Ne peut pas être supprimé",
#     "Ne peut pas être remplacé",
#     "Ne peut pas être ignoré",
#     "Ne peut pas être redirigé",
#     "Ne peut pas être réfléchi",
#     "Touche toujours sous la pluie",
#     "L'utilisateur ne peut pas se retirer",
#     "La cible ne peut pas se retirer",
#     "Attaque KO en un coup",
#     "Modifié contre les Boss",
#     "Aucun effet sur les Boss",
#     "Talent Appât",
#     "Fait contact",
#     "Partiellement implémenté",
#     "Non implémenté",
# ]
helpMenuText = """
<b><span style="color:rgb(140, 130, 240);">Recherche rapide et puissante</span> pour PokeRogue</b>
<hr>
<p style="margin: 10px; font-weight: bold;">Ajoutez des filtres via la <span style="color:rgb(140, 130, 240);">barre de recherche</span>:<br></p>
<p style="margin: 10px; font-weight: bold;"><span style="color:${typeColors[9]};">${catToName[0]}</span>, 
<span style="color:${fidToColor(fidThreshold[0])[0]};">${catToName[1]}</span>,
<span style="color:${fidToColor(fidThreshold[1])[0]};">${catToName[2]}</span>,
<span style="color:${fidToColor(fidThreshold[2])[0]};">${catToName[3]}</span>,
<span style="color:${fidToColor(fidThreshold[3])[0]};">${catToName[4]}</span>,
<span style="color:${fidToColor(fidThreshold[4])[0]};">${catToName[5]}</span>,<br>
<span style="color:${fidToColor(fidThreshold[5])[1]};">${catToName[6]}</span>,
<span style="color:${eggTierColors(2)};">${catToName[7]}</span>,
<span style="color:${fidToColor(fidThreshold[7])[0]};">${headerNames[1]}</span>, ou
<span style="color:${fidToColor(fidThreshold[8])[0]};">${catToName[9]}</span></p>
Combinez plusieurs filtres pour affiner la recherche <br>  
<span style="color:rgb(145, 145, 145);">Cliquez entre eux pour correspondre à l’un ou l’autre</span>
<hr>
<p style="margin: 10px; font-weight: bold;">Cliquez sur les <span style="color:rgb(140, 130, 240);">Entêtes</span> pour trier les résultats</p>
<b>Chromatique</b> peut filtrer les variantes chromatique
<p style="margin: 10px;"><b>${headerNames[4]}</b> peut filtrer un seul slot de talents:<br>
<b>Talents principaux</b>,
<span style="color:rgb(240, 230, 140); font-weight: bold;">Talent caché</span>, ou
<span style="color:rgb(140, 130, 240); font-weight: bold;">Passif</span></p>
<b>${headerNames[5]}</b> affichées comme <b>${fidToName[fidThreshold[6]]}</b> et <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[6]+1]}</span><br>
<span style="color:rgb(145, 145, 145);">Peut aussi afficher la source des mouvements filtrés</span>
<p style="margin: 10px;"><b>${headerNames[6]}</b> affiche la couleur de <b>${catToName[7]}</b>:<br>
<b>${fidToName[fidThreshold[6]]}</b>, <span style="color:rgb(131, 182, 239);"><b>${fidToName[fidThreshold[6]+1]}</b></span>, <span style="color:rgb(240, 230, 140);"><b>${fidToName[fidThreshold[6]+2]}</b></span>, <span style="color:rgb(239, 131, 131);"><b>${fidToName[fidThreshold[6]+3]}</b></span>, <span style="color:rgb(216, 143, 205);"><b>${fidToName[fidThreshold[6]+4]}</b></span></p>
<hr>
<p style="margin: 10px;">Cliquez pour <span style="color:rgb(240, 230, 140); font-weight: bold;">Épingler</span>, ou voir <a href="https://wiki.pokerogue.net/start" target="_blank"><b>Wiki</b></a> ou <span style="color:${fidToColor(fidThreshold[7])[0]}; font-weight: bold;">Variantes</span></p>
<p style="margin: 10px;">Cliquez un <span style="color:rgb(140, 130, 240); font-weight: bold;">${catToName[1]}</span> ou <span style="color:rgb(140, 130, 240); font-weight: bold;">${catToName[2]}</span> pour descriptions</p>
<hr style="margin-bottom: 10px;">
<span style="color:rgb(145, 145, 145); font-size:11px">Ce site a été créé par Sandstorm, et traduit de l'anglais. Je ne collecte pas de données personnelles. Les images et données proviennent de Pokerogue Github. Tous les droits sont réservés à leurs créateurs.</span>
"""