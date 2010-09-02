<?php
require_once('TwitterOAuth.php');
require_once('config.php');

$requestToken = $requestTokenSecrect = null;
$to = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET);
$tok = $to->getRequestToken();

$requestToken = $token = $tok['oauth_token'];
$requestTokenSecrect = $tok['oauth_token_secret'];

$authorizeLink = $to->getAuthorizeURL($token);

echo 'click the following link to authorize your account.', "\n\n";
echo $authorizeLink, "\n\n";

echo "if you have done authorize, type 'yes' to continue: \n";
while(true){
	$handle = fopen ("php://stdin","r");
	if(trim(fgets($handle)) === 'yes'){
		$to = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $requestToken, $requestTokenSecrect);
		$tok = $to->getAccessToken();
		printf("access_token:%s\n", $tok['oauth_token']);
		printf("access_token_secret:%s\n", $tok['oauth_token_secret']);
		exit;
	}
}
