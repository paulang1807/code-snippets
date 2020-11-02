$.getJSON(
  "https://data.cityofnewyork.us/api/views/25th-nujf/rows.json?accessType=DOWNLOAD",
  function (inpData) {
    var user;
    var type;
    console.log("Number of Records: ",inpData.data.length)
    for (i = 0; i < inpData.data.length; i++) {
      user = inpData.data[i];
      if (i % 2 === 0) type = "even";
      else type = "odd";
      $("#users").append(
        '<tr class="' +
          type +
          '"><td>' +
          user[1] +
          "</td><td>" +
          user[11] +
          "</td><td>" +
          user[9] +
          "</td><td>" +
          user[10] +
          '</td><td class="decimal">' +
          user[8] +
          '</td><td class="decimal">' +
          user[12] +
          "</td></tr>"
      );
    }
  }
);
