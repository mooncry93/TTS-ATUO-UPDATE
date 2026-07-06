// --- MASTER CRYPTOGRAPHIC PRIVATE KEYS ---
// ត្រូវប្រាកដថា តម្លៃ d និង n នេះ ត្រូវគ្នានឹងកូដនៅក្នុង master_keys.json របស់អ្នក
const PRIVATE_D = "52478231174557674302076604972543895598923836691698919334180847456091971320836807919389121658763426555104160482410846935649722128780139182686761268035052179202737593715606816159535100634250417365454084519164189531929857146481450541509786062903206757867875375042478335388074731732716685799167925607915090881025";
const RSA_N = "71994847009419654198890424317799696172712974090219423424341340975275784983644509861903767267806382243240906942198398099718989327287768345141242034355848014239571123802198951423502466806124479640775988274631650397754391868448338459527485136220432121760447031679031581472955264566923537232944106854306211726121";

/**
 * បង្កើតប៊ូតុងបញ្ជាពិសេសនៅលើ Google Sheet
 */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('🔑 ប្រព័ន្ធអាជ្ញាប័ណ្ណ')
      .addItem('បើកផ្ទាំងគ្រប់គ្រង (Admin Control Panel)', 'openAdminPanel')
      .addItem('បង្កើត License Key ថ្មី (តាមជួរជ្រើសរើស)', 'generateSelectedLicenses')
      .addToUi();
}

/**
 * បើកផ្ទាំងគ្រប់គ្រងអាជ្ញាប័ណ្ណជា Modal Dialog
 */
function openAdminPanel() {
  var html = HtmlService.createHtmlOutputFromFile('google_sheet_index')
      .setWidth(1150)
      .setHeight(700)
      .setTitle("Digital_TTS - Admin Control Panel")
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  SpreadsheetApp.getUi().showModalDialog(html, '🔑 ផ្ទាំងគ្រប់គ្រងអាជ្ញាប័ណ្ណ (Licensing Admin Console)');
}

/**
 * ច្រកចូលចម្បងសម្រាប់ Web App (doGet API)
 */
function doGet(e) {
  var key = e.parameter.key;
  var action = e.parameter.action;
  
  // ១. ផ្ទៀងផ្ទាត់អាជ្ញាប័ណ្ណតាម API
  if (key && !action) {
    return checkLicenseAPI(key);
  }
  
  // ២. បង្កើតអាជ្ញាប័ណ្ណតាមតំណភ្ជាប់ Web GET Request
  if (action === "generate") {
    return createLicenseAPI(e.parameter.name, e.parameter.hwid, e.parameter.expiry);
  }
  
  // ៣. បង្ហាញផ្ទាំងបញ្ជា HTML Admin Control Panel
  return HtmlService.createHtmlOutputFromFile('google_sheet_index')
                    .setTitle("Digital_TTS - Admin Control Panel")
                    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * ជំនួយការបង្កើត JSON Response
 */
function makeJSONResponse(object) {
  return ContentService.createTextOutput(JSON.stringify(object))
                       .setMimeType(ContentService.MimeType.JSON);
}

/**
 * ស្វែងរកជួរដេកដែលបានជ្រើសរើស រួចបង្កើត License Key ជូនអតិថិជន
 */
function generateSelectedLicenses() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var activeCell = sheet.getActiveCell();
  var row = activeCell.getRow();
  
  if (row == 1) {
    SpreadsheetApp.getUi().alert("សូមជ្រើសរើសជួរដេករបស់អតិថិជន (មិនមែនជួរក្បាលតារាងទេ!)");
    return;
  }
  
  var hwid = sheet.getRange(row, 3).getValue().toString().trim();
  var expiry = sheet.getRange(row, 6).getValue().toString().trim();
  
  if (!hwid || !expiry) {
    SpreadsheetApp.getUi().alert("សូមបញ្ចូល HWID (Column C) និង Expiry (Column F) ជាមុនសិន!");
    return;
  }
  
  var licenseKey = makeKey(hwid, expiry);
  sheet.getRange(row, 1).setValue(licenseKey); // Column A
  sheet.getRange(row, 4).setValue("Active");   // Column D
  SpreadsheetApp.getUi().alert("🎉 បង្កើតបានជោគជ័យ! License Key ត្រូវបានបំពេញក្នុងជួរទី " + row);
}

/**
 * API: ផ្ទៀងផ្ទាត់អាជ្ញាប័ណ្ណរបស់អតិថិជន
 */
function checkLicenseAPI(key) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  
  var key_idx = -1, status_idx = -1;
  for (var i = 0; i < headers.length; i++) {
    var col = headers[i].toString().trim().toLowerCase();
    if (col.indexOf("key") !== -1) key_idx = i;
    if (col.indexOf("status") !== -1) status_idx = i;
  }
  
  if (key_idx === -1 || status_idx === -1) {
    return makeJSONResponse({ "status": "error", "message": "Spreadsheet columns not configured." });
  }
  
  for (var r = 1; r < data.length; r++) {
    var rowKey = data[r][key_idx].toString().trim();
    var rowStatus = data[r][status_idx].toString().trim().toLowerCase();
    
    if (rowKey === key.trim()) {
      if (rowStatus === "revoked" || rowStatus === "blocked" || rowStatus === "inactive") {
        return makeJSONResponse({ "status": "revoked", "message": "License key has been revoked by admin." });
      }
      return makeJSONResponse({ "status": "active", "message": "License verified and active." });
    }
  }
  return makeJSONResponse({ "status": "not_found", "message": "License key not found." });
}

/**
 * API: បង្កើត និងរក្សាទុក License Key ស្វ័យប្រវត្តិតាម URL Parameter
 */
function createLicenseAPI(name, hwid, expiry) {
  if (!hwid || !expiry) {
    return makeJSONResponse({ "success": false, "message": "Missing HWID or Expiry parameters." });
  }
  
  try {
    var licenseKey = makeKey(hwid, expiry);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    sheet.appendRow([
      licenseKey,          // Column A: license_key
      name || "Client Web",// Column B: client_name
      hwid,                // Column C: hwid
      "Active",            // Column D: status
      "Generated via Web API", // Column E: notes
      expiry.toLowerCase() // Column F: expiry
    ]);
    
    return makeJSONResponse({ "success": true, "key": licenseKey });
  } catch(e) {
    return makeJSONResponse({ "success": false, "message": e.toString() });
  }
}

/**
 * មុខងារហៅពី Client-side (google.script.run) ដើម្បីទាញយកទិន្នន័យអាជ្ញាប័ណ្ណទាំងអស់
 */
function getLicenses() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  
  var key_idx = -1, hwid_idx = -1, status_idx = -1, expiry_idx = -1;
  for (var i = 0; i < headers.length; i++) {
    var col = headers[i].toString().trim().toLowerCase();
    if (col.indexOf("key") !== -1) key_idx = i;
    else if (col.indexOf("hwid") !== -1) hwid_idx = i;
    else if (col.indexOf("status") !== -1) status_idx = i;
    else if (col.indexOf("expiry") !== -1) expiry_idx = i;
  }
  
  var licenses = [];
  for (var r = 1; r < data.length; r++) {
    var hwid = hwid_idx !== -1 ? data[r][hwid_idx].toString().trim() : "";
    var key = key_idx !== -1 ? data[r][key_idx].toString().trim() : "";
    var expiry = expiry_idx !== -1 ? data[r][expiry_idx].toString().trim() : "";
    var status = status_idx !== -1 ? data[r][status_idx].toString().trim() : "Inactive";
    
    if (hwid || key) {
      licenses.push({
        hwid: hwid,
        key: key,
        expiry: expiry,
        status: status
      });
    }
  }
  return licenses;
}

/**
 * មុខងារហៅពី Client-side ដើម្បីបង្កើត License Key ថ្មី និងរក្សាទុកក្នុង Sheet
 */
function createLicense(hwid, expiry) {
  if (!hwid || !expiry) {
    throw new Error("Missing HWID or Expiry parameter.");
  }
  var licenseKey = makeKey(hwid, expiry);
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.appendRow([
    licenseKey,                   // Column A: license_key
    "Client Admin",               // Column B: client_name
    hwid,                         // Column C: hwid
    "Active",                     // Column D: status
    "Generated via Admin Panel",  // Column E: notes
    expiry.toString().toLowerCase() // Column F: expiry
  ]);
  return { success: true, key: licenseKey };
}

/**
 * មុខងារហៅពី Client-side ដើម្បីប្ដូរ Status របស់ License (Active/Inactive)
 */
function toggleLicenseStatus(hwid) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  
  var hwid_idx = -1, status_idx = -1;
  for (var i = 0; i < headers.length; i++) {
    var col = headers[i].toString().trim().toLowerCase();
    if (col.indexOf("hwid") !== -1) hwid_idx = i;
    if (col.indexOf("status") !== -1) status_idx = i;
  }
  
  if (hwid_idx === -1 || status_idx === -1) {
    throw new Error("Spreadsheet columns not configured properly.");
  }
  
  for (var r = 1; r < data.length; r++) {
    if (data[r][hwid_idx].toString().trim().toUpperCase() === hwid.trim().toUpperCase()) {
      var currentStatus = data[r][status_idx].toString().trim();
      var newStatus = (currentStatus.toLowerCase() === "active") ? "Inactive" : "Active";
      sheet.getRange(r + 1, status_idx + 1).setValue(newStatus);
      return newStatus;
    }
  }
  throw new Error("License not found.");
}

/**
 * មុខងារហៅពី Client-side ដើម្បីលុប License ចេញពី Sheet
 */
function removeLicense(hwid) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  
  var hwid_idx = -1;
  for (var i = 0; i < headers.length; i++) {
    var col = headers[i].toString().trim().toLowerCase();
    if (col.indexOf("hwid") !== -1) hwid_idx = i;
  }
  
  if (hwid_idx === -1) {
    throw new Error("HWID column not found.");
  }
  
  for (var r = 1; r < data.length; r++) {
    if (data[r][hwid_idx].toString().trim().toUpperCase() === hwid.trim().toUpperCase()) {
      sheet.deleteRow(r + 1);
      return true;
    }
  }
  throw new Error("License not found.");
}

/**
 * មុខងារស្នូលក្នុងការបង្កើត License Key តាមរយៈ RSA Cryptosystem
 */
function makeKey(hwid, expiry) {
  const d = BigInt(PRIVATE_D);
  const n = BigInt(RSA_N);
  
  var license_metadata = {
    "hwid": hwid.trim().toUpperCase(),
    "expiry": expiry.trim().toLowerCase()
  };
  
  var dataStr = JSON.stringify(license_metadata);
  var dataBytes = Utilities.newBlob(dataStr).getBytes();
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, dataStr, Utilities.Charset.UTF_8);
  
  var hashInt = BigInt(0);
  for (var i = 0; i < digest.length; i++) {
    var val = digest[i];
    if (val < 0) val += 256;
    hashInt = (hashInt << BigInt(8)) + BigInt(val);
  }
  
  var signatureInt = power(hashInt, d, n);
  
  var sigBytes = [];
  var temp = signatureInt;
  for (var i = 0; i < 128; i++) {
    var byteVal = Number(temp & BigInt(0xff));
    sigBytes.unshift(byteVal);
    temp = temp >> BigInt(8);
  }
  
  var signedSigBytes = sigBytes.map(function(b) {
    return b > 127 ? b - 256 : b;
  });
  
  var combinedBytes = dataBytes.concat([124, 124]).concat(signedSigBytes);
  var licenseKey = Utilities.base64Encode(combinedBytes);
  
  return licenseKey;
}

/**
 * មុខងារគណនាស្វ័យគុណម៉ូឌុល (Modular Exponentiation)
 */
function power(base, exponent, modulus) {
  var one = BigInt(1);
  var zero = BigInt(0);
  var two = BigInt(2);
  
  if (modulus === one) return zero;
  let result = one;
  base = base % modulus;
  while (exponent > zero) {
    if (exponent % two === one) {
      result = (result * base) % modulus;
    }
    exponent = exponent / two;
    base = (base * base) % modulus;
  }
  return result;
}