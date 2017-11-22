function storeValue(responses, confirmationCode) {
  var ss = SpreadsheetApp.openById(<id of the Google Spreadsheet with the data>);

  // ss is now the spreadsheet the script is associated with
  // var sheet = ss.getSheets()[1]; // sheets are counted starting from 0
  var sheet = ss.getSheetByName("Confirmation");

  // Appends a new row with 6 columns to the bottom of the
  // spreadsheet containing the values in the array
  var arrayData = [responses[0], responses[1], responses[2], responses[3], confirmationCode, 0];
  sheet.appendRow(arrayData);
}

function getMessage(userName, userEmail, userRegion, replyTo) {
  var message = "Thank you very much to select FIWARE Lab Cloud. We have received a request for \n" +
    "FIWARE Lab user creation.\n\n" +
    "Here are the results.\n\n" +
    "Name   " + userName + "\n" +
    "Email	" + userEmail + "\n" +
    "Selected Region " + userRegion + "\n\n" +
    "To confirm that you want to create a FIWARE Lab account, simply reply to this \n" +
    "message, keeping the Subject: header intact.\n\n" +
    "If you do not wish to created a FIWARE Lab account, please simply disregard \n" +
    "this message. If you think you are being maliciously registered to the list, or\n" +
    "have any other questions, send them to " + replyTo + ".\n\n\n" +
    "Thank you very much,\n\n" +
    "FIWARE Lab administrative team.\n\n\n";

  return message;
}

function getErrorMessage(userName, userEmail) {
  var message = "Dear " + userName + ",\n\n" +
    "The domain of your email \"" + userEmail + "\" is not allowed. You cannot register in FIWARE\n" +
    "Lab with it. Please provide other account.\n\n" +
    "FIWARE Lab administrative team.\n\n\n";

  return message;
}

function getCode() {
  var charactersToUse = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
  var varLngthID = 48;
  var confirmationCode = '';

  for (var i=0; i<varLngthID; i++) {
    var randNum = Math.floor(Math.random() * charactersToUse.length);
    confirmationCode += charactersToUse.substring(randNum,randNum+1);
  };

  return confirmationCode;
}

function find(data) {
  var ss = SpreadsheetApp.openById(<id of the Google Spreadsheet with the data>);

  // ss is now the spreadsheet the script is associated with
  var sheet = ss.getSheetByName("Blacklist");
  var range = sheet.getDataRange().getValues();

  var found = 0;

  for(var r=2;r<range.length;++r) {
    var row = range[r],
        name = row[0];

    if(name == data) {
      Logger.log(name)
      found = 1;
      continue;
    }
  }

  Logger.log(found);

  return found;
}

function onFormSubmit(e) {

  responses = e.values;

  // snip //
  var timeStamp = responses[0];
  var userName = responses[1];
  var userEmail = responses[2];
  var userRegion = responses[3];
  var replyTo = 'fiware-lab-user-creation@lists.fiware.org';

  var res = userEmail.split("@");
  var found = find(res[1]);

  if ( found == 0 ) {
    // get the confirmation code
    var confirmationCode = getCode();

    // Update the Confirmation sheet with the data
    storeValue(responses, confirmationCode);

    var subject = "confirm: " + confirmationCode;

    var message = getMessage(userName, userEmail, userRegion, replyTo);

    MailApp.sendEmail (userEmail, replyTo, subject, message);

  } else {
    // Error message due to the domain of the email is inside a blacklist
    var subject = "Error in FIWARE Lab registration";

    var message = getErrorMessage(userName, userEmail);

    MailApp.sendEmail (userEmail, replyTo, subject, message);

  }

}
