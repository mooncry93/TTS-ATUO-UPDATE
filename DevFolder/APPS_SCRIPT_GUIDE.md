# សៀវភៅណែនាំបង្កើត License Key ស្វ័យប្រវត្តិក្នុង Google Sheet (Google Apps Script Guide)

អ្នកអាចបង្កើតអាជ្ញាប័ណ្ណ (License Key) ដោយស្វ័យប្រវត្តិតាមរយៈ Google Sheet ដោយមិនចាំបាច់ដំណើរការស្គ្រីប `keygen.py` នៅលើកុំព្យូទ័រនោះឡើយ។ នៅពេលអ្នកវាយបញ្ចូលលេខ **HWID** និងថ្ងៃកំណត់ **Expiry** នៅក្នុងតារាង Goo## 📝 ជំហានទី ២៖ បញ្ចូលកូដ Google Apps Script (បង្កើត ២ ឯកសារ)

នៅក្នុងផ្ទាំង Apps Script អ្នកត្រូវបង្កើតឯកសារចំនួន ២ ដូចខាងក្រោម៖

### ១. ឯកសារកូដ `Code.gs`៖
1. នៅក្នុង Google Sheet របស់អ្នក ចុចលើម៉ឺនុយ **Extensions** -> **Apps Script**។
2. នៅឯកសារ `Code.gs` សូមលុបកូដចាស់ៗចោល រួចចម្លងកូដខាងក្រោមទៅផាស (Paste) បញ្ចូល៖

```javascript
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
 * បើកផ្ទាំងគ្រប់គ្រងអាជ្ញាប័ណ្ណជា Modal Dialog ដែលមានទំហំធំល្មម (1150x700)
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
 * ច្រកចូលចម្បងសម្រាប់ Web App (doGet)
 */
function doGet(e) {
  var key = e.parameter.key;
  var action = e.parameter.action;
  
  // ១. ផ្ទៀងផ្ទាត់អាជ្ញាប័ណ្ណតាម API
  if (key && !action) {
    return checkLicenseAPI(key);
  }
  
  // ២. បង្កើតអាជ្ញាប័ណ្ណតាមតំណភ្ជាប់ GET URL (សម្រាប់ទម្រង់ HTML Web)
  if (action === "generate") {
    return createLicenseAPI(e.parameter.name, e.parameter.hwid, e.parameter.expiry);
  }
  
  // ៣. បង្ហាញផ្ទាំងបញ្ជា HTML Admin Control Panel (ពី file google_sheet_index.html)
  return HtmlService.createHtmlOutputFromFile('google_sheet_index')
                    .setTitle("Digital_TTS - Admin Control Panel")
                    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
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
 * API: បង្កើត និងរក្សាទុក License Key ស្វ័យប្រវត្តិតាម URL parameter
 */
function createLicenseAPI(name, hwid, expiry) {
  if (!hwid || !expiry) {
    return makeJSONResponse({ "success": false, "message": "Missing HWID or Expiry parameters." });
  }
  
  try {
    var licenseKey = makeKey(hwid, expiry);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // បន្ថែមជួរដេកថ្មីក្នុង Google Sheets ស្វ័យប្រវត្តិ
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
 * មុខងារបង្កើត License Key តាមរយ�3. លុបកូដលំនាំដើមចេញ រួចចម្លងមាតិកាទាំងស្រុងពីឯកសារ [google_sheet_index.html](file:///c:/Users/tntbo/OneDrive/Desktop/TTS/google_sheet_index.html) នៅក្នុងប្រភពកូដ TTS របស់អ្នកមកផាស (Paste) បញ្ចូល។

3. **សំខាន់៖** ជំនួសតម្លៃ `PRIVATE_D` និង `RSA_N` ក្នុងឯកសារ `Code.gs` ដោយចម្លងចេញពីឯកសារ [master_keys.json](file:///c:/Users/tntbo/OneDrive/Desktop/TTS/master_keys.json) របស់អ្នក។
4. ចុចប៊ូតុង **Save** (រូបថាសម៉ាញ៉េទិច) ទាំង ២ ឯកសារ រួចបិទផ្ទាំង Apps Script នោះ។

---

## 🚀 ជំហានទី ៣៖ របៀបប្រើប្រាស់

បន្ទាប់ពីដំឡើងរួចរាល់ អ្នកអាចគ្រប់គ្រងអាជ្ញាប័ណ្ណបាន ២ របៀប៖

### របៀបទី ១៖ ប្រើប្រាស់ផ្ទាំងគ្រប់គ្រងធំ (Admin Control Panel) [ណែនាំ]
1. បើកតារាង Google Sheet របស់អ្នកឡើងវិញ។
2. ចុចម៉ឺនុយ **🔑 ប្រព័ន្ធអាជ្ញាប័ណ្ណ** -> **បើកផ្ទាំងគ្រប់គ្រង (Admin Control Panel)**។
3. ផ្ទាំងគ្រប់គ្រងធំទូលាយ (1150x700) នឹងបង្ហាញឡើង។ អ្នកអាច៖
   * បញ្ចូលលេខ **HWID** និងជ្រើសរើសថ្ងៃផុតកំណត់ រួចចុច **Generate & Save** ដើម្បីបង្កើត key ថ្មីចូល Spreadsheet ភ្លាមៗ។
   * ពិនិត្យមើលបញ្ជីឈ្មោះ និង Key ទាំងអស់ដែលធ្លាប់បានបង្កើត។
   * ចម្លង Key (Copy) ដោយគ្រាន់តែចុចលើ Key នោះ។
   * បិទ ឬបើកអាជ្ញាប័ណ្ណឡើងវិញ (Status Toggle) ដោយគ្រាន់តែចុចលើកុងតាក់ On/Off។
   * លុបអាជ្ញាប័ណ្ណចោលជាអចិន្ត្រៃយ៍។

### របៀបទី ២៖ បង្កើតដោយផ្ទាល់លើតារាង (Sheet-row Keygen)
1. បំពេញឈ្មោះអតិថិជន, លេខ **HWID** (Column C), និងថ្ងៃ **Expiry** (Column F - ទម្រង់៖ `YYYY-MM-DD` ឬ `lifetime`) លើតារាង Sheet។
2. ចុចលើ Cell ណាមួយក្នុងជួរដេករបស់អតិថិជននោះ។
3. ចុចម៉ឺនុយ **🔑 ប្រព័ន្ធអាជ្ញាប័ណ្ណ** -> **បង្កើត License Key ថ្មី (តាមជួរជ្រើសរើស)**។
4. ប្រព័ន្ធនឹងដំណើរការគណនា រួចបំពេញ License Key នៅក្នុង Column A និងប្ដូរ Status ទៅជា "Active" ដោយស្វ័យប្រវត្តិតែម្ដង!

      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> កំពុងគណនា...';
      
      try {
        // រកប្រភព URL បច្ចុប្បន្ននៃ Web App
        const webAppUrl = window.location.href.split("?")[0];
        const requestUrl = \`\${webAppUrl}?action=generate&name=\${encodeURIComponent(name)}&hwid=\${encodeURIComponent(hwid)}&expiry=\${encodeURIComponent(expiry)}\`;
        
        const response = await fetch(requestUrl);
        const resData = await response.json();
        
        if (resData.success) {
          output.value = resData.key;
          resultArea.style.display = "block";
        } else {
          alert("កំហុសក្នុងការបង្កើត៖ " + resData.message);
        }
      } catch (err) {
        alert("កំហុសក្នុងការតភ្ជាប់៖ " + err.toString());
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-circle-plus"></i> បង្កើត License Key';
      }
    }

    function copyKey() {
      const output = document.getElementById("license-output");
      const btn = document.getElementById("btn-copy");
      output.select();
      navigator.clipboard.writeText(output.value).then(() => {
        const origText = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-circle-check" style="color: #06b6d4;"></i> បានចម្លងរួចរាល់!';
        setTimeout(() => {
          btn.innerHTML = origText;
        }, 1500);
      });
    }
  </script>
</body>
</html>`;
}

/**
 * មុខងារជំនួយសម្រាប់គណនាស្វ័យគុណម៉ូឌុល (Modular Exponentiation)
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
```

3. **សំខាន់៖** ជំនួសតម្លៃ `PRIVATE_D` និង `RSA_N` ខាងលើ ដោយចម្លងចេញពីឯកសារ [master_keys.json](file:///Users/mac/Desktop/TTS/master_keys.json) របស់អ្នក។
4. ចុចប៊ូតុង **Save** (រូបថាសម៉ាញ៉េទិច) រួចបិទផ្ទាំង Apps Script នោះ។

---

## 🚀 ជំហានទី ៣៖ របៀបប្រើប្រាស់
1. បើកតារាង Google Sheet របស់អ្នកឡើងវិញ (អ្នកនឹងឃើញម៉ឺនុយថ្មីឈ្មោះ **🔑 ប្រព័ន្ធអាជ្ញាប័ណ្ណ** បង្ហាញនៅរបារខាងលើ)។
2. បំពេញឈ្មោះអតិថិជន, លេខ **HWID** (ចម្លងពីម៉ាស៊ីនអតិថិជន), និងថ្ងៃ **Expiry** (ឧទាហរណ៍៖ `2026-12-31` ឬ `lifetime`)។
3. ចុចលើ Cell ណាមួយក្នុងជួរដេករបស់អតិថិជននោះ។
4. ចុចម៉ឺនុយ **🔑 ប្រព័ន្ធអាជ្ញាប័ណ្ណ** -> **បង្កើត License Key ថ្មី**។
5. ប្រព័ន្ធនឹងដំណើរការគណនា រួចបំពេញ License Key នៅក្នុង Column A និងប្ដូរ Status ទៅជា "Active" ដោយស្វ័យប្រវត្តិតែម្ដង!
6. ចម្លង License Key នោះផ្ញើទៅកាន់អតិថិជនជាការស្រេច។
