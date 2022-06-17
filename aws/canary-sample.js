// Extension for recording steps: https://chrome.google.com/webstore/detail/cloudwatch-synthetics-rec/bhdnlmmgiplmbcdmkkdfplenecpegfno

var synthetics = require('Synthetics');
const log = require('SyntheticsLogger');
const AWS = require('aws-sdk');
const secretsManager = new AWS.SecretsManager();

const test_canary = async function () {
    // INSERT URL here
    let url = "https://www.xyz.com";

    // Get synthetics configuration
    let syntheticsConfig = synthetics.getConfiguration();

    // Set configuration values
    syntheticsConfig.setConfig({
       screenshotOnStepStart : true,
       screenshotOnStepSuccess: true,
       screenshotOnStepFailure: true
    });

  const getSecrets = async (secret_id) => {
    var params = {
        SecretId: secret_id
    };
    return await secretsManager.getSecretValue(params).promise();
    }

  // Fetch secrets
  let secrets = await getSecrets("canary-auth-step3")
  let secretsObj = JSON.parse(secrets.SecretString);

  let page = await synthetics.getPage();

  const navigationPromise = page.waitForNavigation()

  await synthetics.executeStep('navigateToUrl', async function (timeoutInMillis = 60000) {
      await page.goto(url, {waitUntil: 'domcontentloaded', timeout: timeoutInMillis});
  });

  await page.setViewport({ width: 1627, height: 914 })

  await synthetics.executeStep('Type_1', async function() {
    await page.type('.ping-container #identifierInput', "id1")
  })
  
  await synthetics.executeStep('Click_2', async function() {
    await page.waitForSelector('.ping-body-container #btn1')
    await page.click('.ping-body-container #btn1')
  })
  
  await navigationPromise
  
  await synthetics.executeStep('Type_3', async function() {
    await page.type('.ping-body-container #password', secretsObj.password)
  })

  await synthetics.executeStep('Click_4', async function() {
    await page.waitForSelector('div #btn2')
    await page.click('div #btn2')
  })

};
exports.handler = async () => {
    return await test_canary();
};
