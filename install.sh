#!/bin/sh

set -e

# Création de l'nvironnement virtuel avec python 3
# virtualenv --python=python3 venv-ceptyconsultant

# Activation de l'environnement
# source venv-ceptyconsultant/bin/activate

# Installation des dépendances
# pip3 install -r requirements.txt

# Instalation du fichier de configuration
CONFIGFILE="ceptyconsultant.conf"
CONFIGPATH="/etc/nginx/sites-enabled/$CONFIGFILE"

 
edit_config() {
	# Paramétrage SSL
	# defaults paths in UBUNTU :
	# ssl_certificate /etc/ssl/certs/localhost.crt;
	# ssl_certificate_key /etc/ssl/private/localhost.key;
	echo "voulez-vous utiliser les configurations par défaut ? (Y/N)"
	echo "Si oui alors les configuration les configurations suivante seront utilisés :"
	echo "ssl_certificate /etc/ssl/certs/localhost.crt"
	echo "ssl_certificate_key /etc/ssl/private/localhost.key;"
	echo "les fichiers localhost.crt et localhost.key seront copiés automatiquement"

	read resp
	
	if [ $resp = "N" ]; then
		read -p "Entrez l'emplacement de votre fichier ssl_certificate : " SSL_CERT
		read -p "Entrez l'emplacement de votre fichier ssl_certificate_key : " SSL_CERT_KEY
		sed -ri "s|ssl_certificate .*|ssl_certificate $SSL_CERT;|" $CONFIGFILE
		sed -ri "s|ssl_certificate_key .*|ssl_certificate_key $SSL_CERT_KEY;|" $CONFIGFILE
	fi

	if [ $resp = "Y" ]; then
		SSL_CERT=$(pwd)/localhost.crt
		SSL_CERT_KEY=$(pwd)/localhost.key
		sed -ri "s|ssl_certificate .*|ssl_certificate $SSL_CERT;|" $CONFIGFILE
		sed -ri "s|ssl_certificate_key .*|ssl_certificate_key $SSL_CERT_KEY;|" $CONFIGFILE
	fi


	# copie le fichier de configuration à l'emplacement /etc/nginx/sites-enabled/ceptyconsultant.conf
	cp -f $CONFIGFILE $CONFIGPATH
	echo "Le fichier de configuration a été copié avec succès"

	# Remarrage de Nginx pour mettre à jour les congigurations
	echo "Redémarrage de Nginx..."
	systemctl restart nginx
}

if ! [ -f $CONFIGPATH ]; then
	# Si l'utilisateur n'a pas encore de fichier de config à l'emplacement 
	# /etc/nginx/sites-enabled/ceptyconsultant.conf
	edit_config
	cp $CONFIGFILE $CONFIGPATH
	echo "Le fichier de configuration a été copié avec succès"
else 
	# Si l'utilisateur à déjà un fichier de config à l'emplacement 
	# /etc/nginx/sites-enabled/ceptyconsultant.conf
	echo "Le fichier de configuration ceptyconsultant.conf existe déjà à l'emplacement :"
	echo "/etc/nginx/sites-enabled/ceptyconsultant.conf"
	read -p "Voulez-vous le remplacer ? (Y/N) : " resp
	# Si l'utilisateur souhaite modifier son fichier de config
	if [ $resp = "Y" ]; then
		edit_config
	# Si l'utilisateur ne souhaite pas modifier son fichier de config
	else
		echo "Le fichier de configutation n'a pas été modifié"
	fi
fi

echo "Installation terminée"


read -p "Voulez-vous démarrer l'application (Y/N) : " dem
if [ $dem = "Y" ]; then
	sh launcher.sh
fi




