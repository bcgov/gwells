/**

Test from Jenkins Script Console:
evaluate(new File("/var/lib/jenkins/init.groovy.d/000-github-access-token.groovy"))
**/
import jenkins.model.Jenkins;

import com.cloudbees.plugins.credentials.*;
import com.cloudbees.plugins.credentials.impl.*;
import com.cloudbees.plugins.credentials.domains.*;
import org.jenkinsci.plugins.plaincredentials.impl.*;

import hudson.util.Secret;
import com.cloudbees.jenkins.GitHubWebHook;
import com.cloudbees.jenkins.*;
import org.kohsuke.github.*;

import org.jose4j.jws.JsonWebSignature;
import org.jose4j.jws.AlgorithmIdentifiers;
import org.jose4j.jwx.HeaderParameterNames;
import org.jose4j.jwt.JwtClaims;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.spec.PKCS8EncodedKeySpec;
import groovy.json.JsonSlurper;

import java.util.Properties;
import org.apache.commons.io.IOUtils



def createAccessToken = {
    String openshiftPodNamespace=new File('/var/run/pod/namespace').getText('UTF-8').trim()
    String githubSecretName = new File('/var/run/secrets/github/metadata.name').getText('UTF-8').trim()
    String githubAppName = new File('/var/run/secrets/github/app-name').getText('UTF-8').trim()
    String githubAppId = new File('/var/run/secrets/github/app-id').getText('UTF-8').trim()
    String githubInstallationId = new File('/var/run/secrets/github/app-installation-id').getText('UTF-8').trim()
    String githubAppPrivateKey = new File('/var/run/secrets/github/app-private-key').getText('UTF-8').trim()
    
    // convert from PKCS#1 (SSLeay format) to PKCS#8
    //openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in cvarjao-bot.2019-02-21.private-key.pem

    if (!(githubAppPrivateKey.startsWith("-----BEGIN PRIVATE KEY-----") && githubAppPrivateKey.endsWith("-----END PRIVATE KEY-----"))){
        throw new Exception("Invalid private key format. ")
    }

    githubAppPrivateKey = githubAppPrivateKey.replaceAll("\\n", "").replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").replaceAll("\\s+", "");

    byte[] encoded = Base64.getDecoder().decode(githubAppPrivateKey)
    KeyFactory kf = KeyFactory.getInstance("RSA");
    PKCS8EncodedKeySpec keySpecPKCS8 = new PKCS8EncodedKeySpec(encoded);
    PrivateKey privKey = kf.generatePrivate(keySpecPKCS8);
    JwtClaims claims = new JwtClaims();
    claims.setIssuer(githubAppId);
    claims.setIssuedAtToNow();
    claims.setExpirationTimeMinutesInTheFuture(10);

    String payload = claims.toJson();

    //println "PAYLOAD:${payload}"

    JsonWebSignature jsonWebSignature = new JsonWebSignature();
    jsonWebSignature.setPayload(payload);
    jsonWebSignature.setKey(privKey);
    jsonWebSignature.setKeyIdHeaderValue("k1");
    jsonWebSignature.setAlgorithmHeaderValue(AlgorithmIdentifiers.RSA_USING_SHA256);
    jsonWebSignature.setHeader(HeaderParameterNames.TYPE, "JWT");
    String jwt = jsonWebSignature.getCompactSerialization();

    URL url = new URL("https://api.github.com/app/installations/${githubInstallationId}/access_tokens");
    HttpURLConnection con = (HttpURLConnection) url.openConnection();
    con.setRequestMethod("POST");
    con.setRequestProperty("Authorization", "Bearer ${jwt}");
    con.setRequestProperty("Accept", "application/vnd.github.machine-man-preview+json");
    int status = con.getResponseCode();
    String content = IOUtils.toString(con.getInputStream(), 'UTF-8')
    //reader.close();
    con.disconnect();

    //println "CONTENT:\n${content}";
    def accessToken = new JsonSlurper().parseText(content)
    //println "accessToken:\n${accessToken.get("token")}"
    //println "expires_at:\n${accessToken.get("expires_at")}"
    //expires_at
    //GitHub github = new GitHubBuilder().withOAuthToken(accessToken.get("token"), githubAppName).build();
    ['oc','patch', "secret/${githubSecretName}", '-p', '{"stringData": {"password": "'+accessToken.get("token")+'", "token": "'+accessToken.get("token")+'", "expires_at":"'+accessToken.get("expires_at")+'"}}', '-n', openshiftPodNamespace].execute().waitFor()

    return accessToken
}

if (new File('/var/run/secrets/github/app-id').exists()){
    try {
        createAccessToken()
    } catch (Exception exception){
        println("An exception occured during initialization");
        exception.printStackTrace();
        println("Aborting Jenkins ...");
        Jenkins.instance.doExit(null, null);
    }

    //3000000 = 50 minutes
    new Timer().schedule createAccessToken as TimerTask, 3000000, 3000000
}