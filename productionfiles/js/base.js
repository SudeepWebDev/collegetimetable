class ScrollableElement {
  constructor(selector, options = {}) {
    this.element = document.querySelector(selector);
    this.scrollSpeed = options.scrollSpeed || 50;
    this.scrollDirection = options.scrollDirection || 1;
    this.attachScrollListener();
  }

  attachScrollListener() {
    this.element.addEventListener('wheel', (event) => {
      const isAtRightEnd = this.element.scrollLeft + this.element.clientWidth >= this.element.scrollWidth;
      const isAtLeftEnd = this.element.scrollLeft === 0;

      if (isAtRightEnd && event.deltaY > 0) {
        window.scrollBy(0, this.scrollSpeed * this.scrollDirection);
      } else if (isAtLeftEnd && event.deltaY < 0) {
        window.scrollBy(0, -this.scrollSpeed * this.scrollDirection);
      } else {
        const scrollDirection = event.deltaY > 0 ? this.scrollDirection : -this.scrollDirection;
        this.element.scrollLeft += this.scrollSpeed * scrollDirection;
      }

      event.preventDefault();
    });
  }
}

const tableScrollable = new ScrollableElement('.table');

$("#flexSwitchCheckChecked").on("change", function () {
  $("#period-row").toggle(this.checked);
});
const currentPath1 = window.location.pathname;
$("#semesterGroup, #courseGroup, #facultyGroup, #roomGroup, #geGroup, #secGroup, #vacGroup").hide();
$("#courseGroup").show();
$("#course-opt").addClass('click-tag')
if (currentPath1 != "/timetable/") {
  $("#courseGroup").hide();
}

$("#course-opt").on("click", function () {
  $("#courseGroup").show();
  $("#facultyGroup, #geGroup, #roomGroup,#secGroup,#vacGroup").hide();
  $("#course-opt").addClass('click-tag');
  $("#faculty-opt, #ge-opt,#sec-opt,#vac-opt, #room-opt").removeClass('click-tag');
});
$("#faculty-opt").on("click", function () {
  $("#geGroup, #roomGroup, #courseGroup,#secGroup,#vacGroup").hide();
  $("#facultyGroup").show();
  $("#faculty-opt").addClass('click-tag');
  $("#room-opt,#ge-opt,#sec-opt,#vac-opt,#course-opt").removeClass('click-tag');
});
$("#room-opt").on("click", function () {
  $("#geGroup, #courseGroup, #facultyGroup,#secGroup,#vacGroup").hide();
  $("#roomGroup").show();
  $("#room-opt").addClass('click-tag');
  $("#ge-opt,#course-opt,#sec-opt,#vac-opt,#faculty-opt").removeClass('click-tag');
});
$("#ge-opt").on("click", function () {
  $("#geGroup").show();
  $("#roomGroup, #courseGroup, #facultyGroup,#secGroup,#vacGroup").hide();
  $("#ge-opt").addClass('click-tag');
  $("#sec-opt,#vac-opt,#course-opt,#room-opt,#faculty-opt").removeClass('click-tag');
});
$("#sec-opt").on("click", function () {
  $("#secGroup").show();
  $("#roomGroup, #courseGroup, #facultyGroup,#geGroup,#vacGroup").hide();
  $("#sec-opt").addClass('click-tag');
  $("#ge-opt,#vac-opt,#course-opt,#room-opt,#faculty-opt").removeClass('click-tag');
});
$("#vac-opt").on("click", function () {
  $("#vacGroup").show();
  $("#roomGroup, #courseGroup, #facultyGroup,#geGroup,#secGroup").hide();
  $("#vac-opt").addClass('click-tag');
  $("#ge-opt,#sec-opt,#course-opt,#room-opt,#faculty-opt").removeClass('click-tag');
});

let faculty, room, course, semester, section, sectionge, sectionsec, sectionvac, semesterge, semestersec, semestervac, paperge, papersec, papervac;

function showAlert(message) {
  $("#alertMessage").text(message);
  $("#alert").show();
}

function hideAlert() {
  $("#alert").attr('style', 'display:none !important');
}

$("#submit-tt-btn").on("click", function (e) {
  e.preventDefault();

  semester = $("#semester").val();
  semesterge = $("#semesterge").val();
  semestersec = $("#semestersec").val();
  semestervac = $("#semestervac").val();
  paperge = $("#paperge").val();
  papersec = $("#papersec").val();
  papervac = $("#papervac").val();
  course = $("#course").val();
  faculty = $("#faculty").val();
  room = $("#room").val();
  section = $("#section").val();
  sectionge = $("#sectionge").val();
  sectionsec = $("#sectionsec").val();
  sectionvac = $("#sectionvac").val();

  let errorMessage = "";

  if ($("#facultyGroup").is(":visible") && faculty === null) {
    errorMessage = "Please select a faculty.";
  } else if ($("#roomGroup").is(":visible") && room === null) {
    errorMessage = "Please select a room.";
  } else if ($("#courseGroup").is(":visible") && (course === null || semester === null || section === null)) {
    errorMessage = "Please select semester, course, and section.";
  } else if ($("#geGroup").is(":visible") && (paperge === null || semesterge === null || sectionge === null)) {
    errorMessage = "Please select semester, section and paper for GE.";
  } else if ($("#secGroup").is(":visible") && (papersec === null || semestersec === null || sectionsec === null)) {
    errorMessage = "Please select semester, section and paper for SEC.";
  } else if ($("#vacGroup").is(":visible") && (papervac === null || semestervac === null || sectionvac === null)) {
    errorMessage = "Please select semester, section and paper for VAC.";
  }

  if (errorMessage !== "") {
    showAlert(errorMessage);
    setTimeout(hideAlert, 5000);
  } else {
    redirectBasedOnSelection();
  }
});

function redirectBasedOnSelection() {
  if ($("#facultyGroup").is(":visible") && faculty !== null) {
    window.location.href = "/timetable/faculty/" + faculty + "/";
  } else if ($("#roomGroup").is(":visible") && room !== null) {
    window.location.href = "/timetable/room/" + room + "/";
  } else if ($("#courseGroup").is(":visible") && course !== null && semester !== null && section !== null) {
    window.location.href = "/timetable/course/" + semester + "/" + course + "/" + section + "/";
  } else if ($("#geGroup").is(":visible") && paperge !== null && semesterge !== null) {
    window.location.href = "/timetable/gvs/" + paperge + "/" + sectionge + "/" + semesterge + "/";
  } else if ($("#secGroup").is(":visible") && papersec !== null && semestersec !== null) {
    window.location.href = "/timetable/gvs/" + papersec + "/" + sectionsec + "/" + semestersec + "/";
  } else if ($("#vacGroup").is(":visible") && papervac !== null && semestervac !== null) {
    window.location.href = "/timetable/gvs/" + papervac + "/" + sectionvac + "/" + semestervac + "/";
  }
}

const currentPath = window.location.pathname;
if (currentPath == "/timetable/") {
  $("#tt-container").hide();
}
if (currentPath.startsWith("/timetable/") && currentPath !== "/timetable/") {
  $("#reselect-tt-btn").show();
  $("#selectOption").attr('style', 'display:none !important');
  $("#submit-tt-btn").hide();
}
if ($("#reselect-tt-btn")) {
  $("#reselect-tt-btn").on("click", function () {
    window.location.href = "/timetable/";
  })
}

const cap = $("#table-title");

const selected_val = $("#selectedvalue");
const pathSegments = currentPath.split('/');
const retrived_tt_val = pathSegments[pathSegments.length - 3];
var spanElement = $("<span>").addClass("padding-15px-lr padding-5px-tb border flex-grow-1")
  .css("font-weight", "600");
if (cap.length > 0) {
  if (pathSegments[pathSegments.length - 4] == "faculty") {
    cap.text("Faculty Name: " + decodeURIComponent(pathSegments[pathSegments.length - 2]));
    spanElement.text("Faculty Name: " + decodeURIComponent(pathSegments[pathSegments.length - 2]));
    selected_val.append(spanElement);
  } else if (pathSegments[pathSegments.length - 3] == "room") {
    cap.text("Room Number: " + decodeURIComponent(pathSegments[pathSegments.length - 2]));
    spanElement.text("Room Number: " + decodeURIComponent(pathSegments[pathSegments.length - 2]));
    selected_val.append(spanElement);
  } else if (pathSegments[pathSegments.length - 5] == "course") {
    cap.text("Course: " + decodeURIComponent(retrived_tt_val) + " || " + "Semester: " + decodeURIComponent(pathSegments[pathSegments.length - 4]) + " || " + "Section: " + decodeURIComponent(pathSegments[pathSegments.length - 2]));
    spanElement.text("Course: " + decodeURIComponent(retrived_tt_val) + " || " + "Semester: " + decodeURIComponent(pathSegments[pathSegments.length - 4]) + " || " + "Section: " + decodeURIComponent(pathSegments[pathSegments.length - 2]));
    selected_val.append(spanElement);
  } else if (pathSegments[pathSegments.length - 5] == "gvs") {
    cap.text("Section: " + decodeURIComponent(retrived_tt_val) + " || " + "Paper: " + decodeURIComponent(pathSegments[pathSegments.length - 4]) + " || " + "Semester: " + decodeURIComponent(pathSegments[pathSegments.length - 2]));
    spanElement.text("Section: " + decodeURIComponent(retrived_tt_val) + " || " + "Paper: " + decodeURIComponent(pathSegments[pathSegments.length - 4]) + " || " + "Semester: " + decodeURIComponent(pathSegments[pathSegments.length - 2]));
    selected_val.append(spanElement);
  }
}
const printBtn = document.getElementById('download-tt-btn');
if (printBtn) {
  printBtn.addEventListener('click', function toPDF() {
    const element = document.getElementById('timetable-table');

    html2canvas(element).then(canvas => {
      const imageData = canvas.toDataURL('image/png');
      const img = new Image();
      img.src = imageData;
      const downloadLink = document.createElement('a');
      downloadLink.href = imageData;
      downloadLink.download = 'timetable.png';
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    });
  })
}


$("#selectOption span").click(function () {
  var selectedOption = $(this).attr('id');
  $.ajax({
    url: '/timetable/',
    data: { 'option': selectedOption },
    dataType: 'html',
    success: function (data) {
      var groupMap = {
        'faculty-opt': '#facultyGroup',
        'sec-opt': '#secGroup',
        'ge-opt': '#geGroup',
        'room-opt': '#roomGroup',
        'vac-opt': '#vacGroup',
      };
      var groupID = groupMap[selectedOption];
      $(groupID).html(data);
    }
  });
});
