#!/usr/bin/env python3
"""Génère les pages du site (nav et pied de page communs). Usage : python3 outils/build.py"""
import re, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://webaunet.github.io/antoine-garden-care/"
TEL, TELH = "06 35 27 06 51", "tel:+33635270651"
FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2327432f'/%3E%3Cpath d='M32 50V30M32 30c0-10 8-16 18-16 0 10-8 16-18 16zM32 38c0-8-6-12-14-12 0 8 6 12 14 12z' fill='none' stroke='%23f7f2e8' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")
MENU = [("index.html", "Accueil"), ("prestations.html", "Prestations"), ("a-propos.html", "À propos"), ("contact.html", "Contact")]

def page(fname, title, desc, main, cur):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a></li>' for h, t in MENU)
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="{FAV}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<header class="site-header" id="accueil">
  <div class="wrap nav">
    <a class="logo" href="{BASE}" aria-label="Antoine Garden Care, accueil">Antoine Garden Care</a>
    <a class="btn btn-terre nav-cta" href="{TELH}" aria-label="Appeler le {TEL}"><span class="t-long">{TEL}</span><span class="t-court">Appeler</span></a>
    <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span></button>
    <ul class="menu" id="menu">{items}</ul>
  </div>
</header>
<main>
{main}
</main>
<footer class="site-footer">
  <div class="wrap foot">
    <span>© Antoine Garden Care · 40 rue des Vignobles, 78400 Chatou · <a href="{TELH}">{TEL}</a></span>
    <nav aria-label="Pied de page"><a href="prestations.html">Prestations</a><a href="a-propos.html">À propos</a><a href="contact.html">Contact</a><a href="mentions-legales.html">Mentions légales</a></nav>
  </div>
</footer>
<script src="js/site.js"></script>
</body>
</html>
'''

def w(name, html):
    open(os.path.join(R, name), "w", encoding="utf-8").write(html)

# ---------- ACCUEIL : on réutilise le <main> validé ----------
idx = open(os.path.join(R, "index.html"), encoding="utf-8").read()
m = re.search(r"<main>\n(.*)\n</main>", idx, re.S)
home = m.group(1)
home = home.replace('href="#contact"', f'href="contact.html"')
home = home.replace('href="#accueil">Retour en haut', 'href="#accueil">Retour en haut')
w("index.html", page("index.html", "Antoine Garden Care – Paysagiste à Chatou (78)",
  "Antoine Garden Care, entreprise d'aménagement paysager à Chatou (Yvelines) : aménagement et entretien de jardins. Contactez-nous au 06 35 27 06 51.",
  home, "index.html"))

# ---------- PRESTATIONS ----------
presta = '''
<section class="ph" aria-labelledby="t">
  <div class="wrap ph-grid">
    <div>
      <span class="eyebrow">Prestations</span>
      <h1 id="t">Ce que nous faisons dans votre jardin.</h1>
      <p class="lead">Un volet pour construire et planter, un volet pour entretenir. Choisissez celui qui vous concerne.</p>
      <div class="hero-actions"><a class="btn btn-terre" href="#amenager">Aménager</a><a class="btn btn-vert" href="#entretenir">Entretenir</a></div>
    </div>
    <div class="mosaique">
      <img src="images/hero-allee-paves.jpg" width="1400" height="764" alt="Allée de dalles de pierre longeant un muret fleuri" class="m1">
      <img src="images/jardin-robot-tonte.jpg" width="1400" height="764" alt="Jardin avec muret de pierre, terrasse et allée pavée" class="m2" loading="lazy">
      <img src="images/conception-tablette.jpg" width="1100" height="600" alt="Plan de jardin en 3D présenté sur une tablette" class="m3" loading="lazy">
    </div>
  </div>
</section>

<section class="zig" id="amenager" aria-labelledby="t-am">
  <div class="wrap">
    <span class="eyebrow">Volet 1</span>
    <h2 id="t-am">Aménager : construire l'extérieur.</h2>
    <div class="rang">
      <img loading="lazy" src="images/terrasse-bois.jpg" width="900" height="491" alt="Pose des lames d'une terrasse en bois devant une maison en pierre">
      <div><h3>Terrasses</h3><p>Une terrasse en bois pour manger, recevoir ou simplement profiter du jardin, posée au plus près de la maison.</p></div>
    </div>
    <div class="rang inverse">
      <img loading="lazy" src="images/allee-dallee.jpg" width="900" height="491" alt="Allée dallée en pierre éclairée par des bornes lumineuses">
      <div><h3>Allées et cheminements</h3><p>Dalles ou pavés pour relier la maison au jardin, avec un éclairage discret pour les soirées.</p></div>
    </div>
  </div>
</section>

<section class="plant" aria-labelledby="t-pl">
  <div class="wrap">
    <span class="eyebrow">Volet 1, suite</span>
    <h2 id="t-pl">Structurer, préparer le sol, planter.</h2>
    <div class="trio">
      <article><img loading="lazy" src="images/muret-pierre.jpg" width="900" height="491" alt="Montage d'un muret et d'un escalier en pierre dans un jardin en pente"><div><h3>Maçonnerie paysagère</h3><p>Murets, marches et soutènements en pierre pour structurer un terrain et créer des niveaux.</p></div></article>
      <article><img loading="lazy" src="images/terrassement.jpg" width="900" height="502" alt="Terrassement d'une partie de pelouse à la pelle, devant une maison"><div><h3>Terrassement et nivellement</h3><p>On prépare le terrain avant tout aménagement : on creuse, on nivelle, on met le sol à niveau.</p></div></article>
      <article><img loading="lazy" src="images/plantation.jpg" width="900" height="491" alt="Mise en terre d'un arbuste dans un massif de vivaces"><div><h3>Plantations et massifs</h3><p>Choix et mise en place des plantes, création de massifs et de bordures qui tiennent dans le temps.</p></div></article>
    </div>
  </div>
</section>

<section class="entretien" id="entretenir" aria-labelledby="t-en">
  <div class="wrap">
    <span class="eyebrow">Volet 2</span>
    <h2 id="t-en">Entretenir : un jardin qui reste beau.</h2>
    <p class="lead">Des passages réguliers ou ponctuels, selon vos besoins.</p>
    <div class="grille6">
      <article><img loading="lazy" src="images/tonte-pelouse.jpg" width="900" height="502" alt="Tonte d'une pelouse le long d'une haie"><h3>Tonte</h3></article>
      <article><img loading="lazy" src="images/taille-haie.jpg" width="900" height="491" alt="Taille d'une haie au taille-haie"><h3>Taille de haies</h3></article>
      <article><img loading="lazy" src="images/desherbage-massif.jpg" width="900" height="491" alt="Désherbage d'un massif fleuri"><h3>Désherbage</h3></article>
      <article><img loading="lazy" src="images/feuilles-allee.jpg" width="900" height="491" alt="Ramassage de feuilles mortes sur une allée gravillonnée"><h3>Ramassage des feuilles</h3></article>
      <article><img loading="lazy" src="images/dechets-verts.jpg" width="900" height="491" alt="Chargement de déchets verts dans une camionnette"><h3>Déchets verts</h3></article>
      <article><img loading="lazy" src="images/entretien-general.jpg" width="900" height="502" alt="Tonte d'une pelouse devant une maison en pierre"><h3>Entretien général</h3></article>
    </div>
  </div>
</section>

<section class="bandeau" aria-labelledby="t-b">
  <div class="wrap">
    <h2 id="t-b">Votre projet ne rentre pas dans une case ?</h2>
    <p>Appelez-nous : on regarde ensemble ce qui est possible chez vous.</p>
    <div class="hero-actions"><a class="btn btn-clair" href="tel:+33635270651">Appeler le 06 35 27 06 51</a><a class="btn btn-contour" href="contact.html">Préparer ma demande</a></div>
  </div>
</section>'''
w("prestations.html", page("prestations.html", "Prestations – Antoine Garden Care, paysagiste à Chatou",
  "Aménagement (terrasses, allées, murets, plantations) et entretien (tonte, haies, désherbage) de jardins à Chatou, Yvelines. Antoine Garden Care.",
  presta, "prestations.html"))

# ---------- A PROPOS ----------
apropos = '''
<section class="ap-head" aria-labelledby="t">
  <div class="wrap ap-grid">
    <div>
      <span class="eyebrow">À propos</span>
      <h1 id="t">Le jardin, c'est notre métier.</h1>
      <p class="lead">Antoine Garden Care est une entreprise de services d'aménagement paysager installée à Chatou, dans les Yvelines. Elle intervient sur l'aménagement comme sur l'entretien des jardins.</p>
      <div class="hero-actions"><a class="btn btn-terre" href="tel:+33635270651">Appeler</a><a class="btn btn-vert" href="prestations.html">Voir les prestations</a></div>
    </div>
    <img src="images/jardin-entretenu.jpg" width="900" height="491" alt="Jardin soigné avec pelouse, massifs et allée de gravier devant une maison ancienne">
  </div>
</section>

<section class="ap-etapes" aria-labelledby="t2">
  <div class="wrap">
    <h2 id="t2">Comment une demande se déroule.</h2>
    <div class="frise">
      <div class="f"><span>1</span><h3>Vous appelez</h3><p>Vous nous décrivez votre jardin et ce que vous souhaitez.</p></div>
      <div class="f"><span>2</span><h3>On se met d'accord</h3><p>Nous précisons ensemble le projet avant d'intervenir.</p></div>
      <div class="f"><span>3</span><h3>On intervient</h3><p>Chantier ou passage d'entretien, selon la demande.</p></div>
    </div>
  </div>
</section>

<section class="ap-id" aria-labelledby="t3">
  <div class="wrap ap-id-grid">
    <div>
      <h2 id="t3">L'entreprise en bref.</h2>
      <p class="lead">Les informations ci-contre proviennent du registre officiel des entreprises.</p>
    </div>
    <dl class="fiche">
      <div><dt>Nom</dt><dd>Antoine Garden Care</dd></div>
      <div><dt>Activité</dt><dd>Services d'aménagement paysager</dd></div>
      <div><dt>Siège</dt><dd>40 rue des Vignobles, 78400 Chatou</dd></div>
      <div><dt>SIREN</dt><dd>504 455 049</dd></div>
      <div><dt>Téléphone</dt><dd><a href="tel:+33635270651">06 35 27 06 51</a></dd></div>
    </dl>
  </div>
</section>

<section class="bandeau vert" aria-labelledby="t4">
  <div class="wrap">
    <h2 id="t4">Faisons connaissance au téléphone.</h2>
    <p>Un échange de quelques minutes suffit pour savoir si nous pouvons vous aider.</p>
    <div class="hero-actions"><a class="btn btn-terre" href="tel:+33635270651">06 35 27 06 51</a></div>
  </div>
</section>'''
w("a-propos.html", page("a-propos.html", "À propos – Antoine Garden Care, aménagement paysager à Chatou",
  "Antoine Garden Care, entreprise d'aménagement paysager basée rue des Vignobles à Chatou (78). Informations de l'entreprise et déroulé d'une demande.",
  apropos, "a-propos.html"))

# ---------- CONTACT ----------
contact = '''
<section class="ct" aria-labelledby="t">
  <div class="wrap ct-grid">
    <div class="ct-form">
      <span class="eyebrow">Contact</span>
      <h1 id="t">Parlons de votre jardin.</h1>
      <p class="lead">Remplissez ce formulaire : il prépare un message prêt à envoyer par SMS, à copier ou à dire au téléphone.</p>
      <form id="f" novalidate>
        <div class="champ"><label for="nom">Nom *</label><input id="nom" name="nom" autocomplete="name" required aria-describedby="e-nom"><p class="err" id="e-nom" role="alert"></p></div>
        <div class="champ"><label for="tel">Téléphone *</label><input id="tel" name="tel" type="tel" inputmode="tel" autocomplete="tel" required placeholder="06 12 34 56 78" aria-describedby="e-tel"><p class="err" id="e-tel" role="alert"></p></div>
        <div class="champ"><label for="type">Votre besoin *</label>
          <select id="type" name="type" required aria-describedby="e-type"><option value="">Choisir…</option><option>Aménagement (terrasse, allée, muret, plantations…)</option><option>Entretien (tonte, haies, désherbage…)</option><option>Autre demande</option></select><p class="err" id="e-type" role="alert"></p></div>
        <div class="champ"><label for="msg">Votre projet *</label><textarea id="msg" name="msg" rows="4" required aria-describedby="e-msg"></textarea><p class="err" id="e-msg" role="alert"></p></div>
        <button class="btn btn-terre" type="submit">Préparer mon message</button>
      </form>
      <div class="recap" id="recap" hidden tabindex="-1" aria-live="polite">
        <h2>Votre message est prêt</h2>
        <pre id="recap-txt"></pre>
        <div class="hero-actions"><a class="btn btn-terre" id="sms" href="#">Envoyer par SMS</a><button class="btn btn-vert" id="copier" type="button">Copier</button><a class="btn btn-contour-v" href="tel:+33635270651">Appeler</a></div>
        <p class="ok" id="ok" role="status"></p>
      </div>
    </div>
    <aside class="ct-side">
      <img loading="lazy" src="images/feuilles-allee.jpg" width="900" height="491" alt="Ramassage de feuilles sur une allée gravillonnée dans un jardin">
      <div class="coords">
        <h2>Nous joindre</h2>
        <p><strong>Téléphone</strong><br><a href="tel:+33635270651">06 35 27 06 51</a></p>
        <p><strong>Adresse</strong><br>40 rue des Vignobles<br>78400 Chatou</p>
      </div>
    </aside>
  </div>
</section>'''
w("contact.html", page("contact.html", "Contact – Antoine Garden Care, paysagiste à Chatou",
  "Contactez Antoine Garden Care à Chatou (78) : appel au 06 35 27 06 51 ou message préparé en ligne à envoyer par SMS.",
  contact, "contact.html").replace('<script src="js/site.js"></script>', '<script src="js/site.js"></script>\n<script src="js/contact.js"></script>'))

# ---------- MENTIONS LEGALES ----------
ml = '''
<section class="legal" aria-labelledby="t">
  <div class="wrap legal-in">
    <h1 id="t">Mentions légales</h1>
    <p class="lead">Ce site est une maquette de démonstration. Seules les informations vérifiées sont indiquées ci-dessous.</p>
    <h2>Entreprise</h2>
    <dl class="fiche">
      <div><dt>Dénomination</dt><dd>Antoine Garden Care</dd></div>
      <div><dt>SIREN</dt><dd>504 455 049</dd></div>
      <div><dt>Adresse</dt><dd>40 rue des Vignobles, 78400 Chatou</dd></div>
      <div><dt>Téléphone</dt><dd><a href="tel:+33635270651">06 35 27 06 51</a></dd></div>
    </dl>
    <h2>Informations à compléter</h2>
    <p>Forme juridique, nom du responsable de la publication, adresse e-mail, numéro de TVA et hébergeur ne sont pas renseignés à ce stade : ils devront être fournis par l'entreprise avant toute mise en ligne définitive.</p>
    <h2>Images</h2>
    <p>Les images de cette maquette sont illustratives et ne représentent pas des réalisations de l'entreprise.</p>
  </div>
</section>'''
w("mentions-legales.html", page("mentions-legales.html", "Mentions légales – Antoine Garden Care, Chatou",
  "Mentions légales du site d'Antoine Garden Care, entreprise d'aménagement paysager à Chatou (78).", ml, "mentions-legales.html"))
print("ok")
