/* =========================================================
   WELLSPRING HOSPITAL MANAGEMENT SYSTEM
   JavaScript
========================================================= */


/* =========================================================
   COMMON MODAL FUNCTIONS
========================================================= */

function openModal(id) {
    const modal = document.getElementById(id);

    if (modal) {
        modal.classList.add("active");
        document.body.style.overflow = "hidden";
    }
}


function closeModal(id) {
    const modal = document.getElementById(id);

    if (modal) {
        modal.classList.remove("active");
        document.body.style.overflow = "";
    }
}


/* Close modal when clicking outside */

document.addEventListener("click", function (event) {

    if (event.target.classList.contains("modal-overlay")) {
        event.target.classList.remove("active");
        document.body.style.overflow = "";
    }

});


/* Close modal using Escape key */

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        const activeModal = document.querySelector(
            ".modal-overlay.active"
        );

        if (activeModal) {
            activeModal.classList.remove("active");
            document.body.style.overflow = "";
        }

    }

});


/* =========================================================
   PATIENTS
========================================================= */

function openAddPatientModal() {
    openModal("addPatientModal");
}


function closeAddPatientModal() {
    closeModal("addPatientModal");
}


function viewPatient(
    id,
    name,
    age,
    gender,
    phone,
    bloodGroup,
    department,
    address
) {

    document.getElementById("viewPatientAvatar").textContent =
        name ? name.charAt(0).toUpperCase() : "P";

    document.getElementById("viewPatientName").textContent =
        name || "-";

    document.getElementById("viewPatientId").textContent =
        "#" + id;

    document.getElementById("viewPatientAge").textContent =
        age || "-";

    document.getElementById("viewPatientGender").textContent =
        gender || "-";

    document.getElementById("viewPatientPhone").textContent =
        phone || "-";

    document.getElementById("viewPatientBloodGroup").textContent =
        bloodGroup || "-";

    document.getElementById("viewPatientDepartment").textContent =
        department || "-";

    document.getElementById("viewPatientAddress").textContent =
        address || "-";

    openModal("viewPatientModal");
}


function closeViewPatientModal() {
    closeModal("viewPatientModal");
}


function editPatient(
    id,
    name,
    age,
    gender,
    phone,
    bloodGroup,
    department,
    address
) {

    document.getElementById("editPatientForm").action =
        "/edit_patient/" + id;

    document.getElementById("editPatientName").value =
        name || "";

    document.getElementById("editPatientAge").value =
        age || "";

    document.getElementById("editPatientGender").value =
        gender || "";

    document.getElementById("editPatientPhone").value =
        phone || "";

    document.getElementById("editPatientBloodGroup").value =
        bloodGroup || "";

    document.getElementById("editPatientDepartment").value =
        department || "";

    document.getElementById("editPatientAddress").value =
        address || "";

    openModal("editPatientModal");
}


function closeEditPatientModal() {
    closeModal("editPatientModal");
}


function confirmDeletePatient(id, name) {

    document.getElementById("deletePatientForm").action =
        "/delete_patient/" + id;

    document.getElementById("deletePatientName").textContent =
        name || "this patient";

    openModal("deletePatientModal");
}


function closeDeletePatientModal() {
    closeModal("deletePatientModal");
}


/* Patient live search */

function filterPatients() {

    const input = document.getElementById("patientSearch");
    const table = document.getElementById("patientsTable");

    if (!input || !table) {
        return;
    }

    const searchValue = input.value.toLowerCase().trim();
    const rows = table.querySelectorAll("tbody tr");

    rows.forEach(function (row) {

        const text = row.textContent.toLowerCase();

        row.style.display =
            text.includes(searchValue) ? "" : "none";

    });
}


/* =========================================================
   DOCTORS
========================================================= */

function openAddDoctorModal() {
    openModal("addDoctorModal");
}


function closeAddDoctorModal() {
    closeModal("addDoctorModal");
}


function viewDoctor(
    id,
    name,
    specialization,
    experience,
    phone,
    email,
    status
) {

    document.getElementById("viewDoctorAvatar").textContent =
        name ? name.charAt(0).toUpperCase() : "D";

    document.getElementById("viewDoctorName").textContent =
        name || "-";

    document.getElementById("viewDoctorId").textContent =
        "#" + id;

    document.getElementById("viewDoctorSpecialization").textContent =
        specialization || "-";

    document.getElementById("viewDoctorExperience").textContent =
        experience || "-";

    document.getElementById("viewDoctorPhone").textContent =
        phone || "-";

    document.getElementById("viewDoctorEmail").textContent =
        email || "-";

    document.getElementById("viewDoctorStatus").textContent =
        status || "-";

    openModal("viewDoctorModal");
}


function closeViewDoctorModal() {
    closeModal("viewDoctorModal");
}


function editDoctor(
    id,
    name,
    specialization,
    experience,
    phone,
    email,
    status
) {

    document.getElementById("editDoctorForm").action =
        "/edit_doctor/" + id;

    document.getElementById("editDoctorName").value =
        name || "";

    document.getElementById("editDoctorSpecialization").value =
        specialization || "";

    document.getElementById("editDoctorExperience").value =
        experience || "";

    document.getElementById("editDoctorPhone").value =
        phone || "";

    document.getElementById("editDoctorEmail").value =
        email || "";

    document.getElementById("editDoctorStatus").value =
        status || "";

    openModal("editDoctorModal");
}


function closeEditDoctorModal() {
    closeModal("editDoctorModal");
}


function confirmDeleteDoctor(id, name) {

    document.getElementById("deleteDoctorForm").action =
        "/delete_doctor/" + id;

    document.getElementById("deleteDoctorName").textContent =
        name || "this doctor";

    openModal("deleteDoctorModal");
}


function closeDeleteDoctorModal() {
    closeModal("deleteDoctorModal");
}


/* Doctor live search */

function filterDoctors() {

    const input = document.getElementById("doctorSearch");
    const table = document.getElementById("doctorsTable");

    if (!input || !table) {
        return;
    }

    const searchValue = input.value.toLowerCase().trim();
    const rows = table.querySelectorAll("tbody tr");

    rows.forEach(function (row) {

        const text = row.textContent.toLowerCase();

        row.style.display =
            text.includes(searchValue) ? "" : "none";

    });
}


/* =========================================================
   APPOINTMENTS
========================================================= */

function openAddAppointmentModal() {
    openModal("addAppointmentModal");
}


function closeAddAppointmentModal() {
    closeModal("addAppointmentModal");
}


function viewAppointment(
    id,
    patientName,
    doctorName,
    date,
    time,
    department,
    reason,
    status
) {

    document.getElementById("viewAppointmentAvatar").textContent =
        patientName
            ? patientName.charAt(0).toUpperCase()
            : "P";

    document.getElementById("viewAppointmentPatient").textContent =
        patientName || "-";

    document.getElementById("viewAppointmentId").textContent =
        "#" + id;

    document.getElementById("viewAppointmentDoctor").textContent =
        doctorName || "-";

    document.getElementById("viewAppointmentDepartment").textContent =
        department || "-";

    document.getElementById("viewAppointmentDate").textContent =
        date || "-";

    document.getElementById("viewAppointmentTime").textContent =
        time || "-";

    document.getElementById("viewAppointmentStatus").textContent =
        status || "-";

    document.getElementById("viewAppointmentReason").textContent =
        reason || "-";

    openModal("viewAppointmentModal");
}


function closeViewAppointmentModal() {
    closeModal("viewAppointmentModal");
}


function editAppointment(
    id,
    patientName,
    doctorName,
    date,
    time,
    department,
    reason
) {

    document.getElementById("editAppointmentForm").action =
        "/edit_appointment/" + id;

    document.getElementById("editAppointmentPatient").value =
        patientName || "";

    document.getElementById("editAppointmentDoctor").value =
        doctorName || "";

    document.getElementById("editAppointmentDate").value =
        date || "";

    document.getElementById("editAppointmentTime").value =
        time || "";

    document.getElementById("editAppointmentDepartment").value =
        department || "";

    document.getElementById("editAppointmentReason").value =
        reason || "";

    openModal("editAppointmentModal");
}


function closeEditAppointmentModal() {
    closeModal("editAppointmentModal");
}


/* Reschedule cancelled appointment */

function rescheduleAppointment(
    id,
    patientName,
    doctorName,
    date,
    time
) {

    document.getElementById("rescheduleAppointmentForm").action =
        "/reschedule_appointment/" + id;

    document.getElementById("reschedulePatient").textContent =
        patientName || "-";

    document.getElementById("rescheduleDoctor").textContent =
        doctorName || "-";

    document.getElementById("rescheduleDate").value =
        date || "";

    document.getElementById("rescheduleTime").value =
        time || "";

    openModal("rescheduleAppointmentModal");
}


function closeRescheduleAppointmentModal() {
    closeModal("rescheduleAppointmentModal");
}


/* Cancel appointment */

function confirmCancelAppointment(id, patientName) {

    document.getElementById("cancelAppointmentForm").action =
        "/cancel_appointment/" + id;

    document.getElementById("cancelAppointmentName").textContent =
        patientName || "this appointment";

    openModal("cancelAppointmentModal");
}


function closeCancelAppointmentModal() {
    closeModal("cancelAppointmentModal");
}


/* Appointment live search */

function filterAppointments() {

    const input = document.getElementById("appointmentSearch");
    const table = document.getElementById("appointmentsTable");

    if (!input || !table) {
        return;
    }

    const searchValue = input.value.toLowerCase().trim();
    const rows = table.querySelectorAll("tbody tr");

    rows.forEach(function (row) {

        const text = row.textContent.toLowerCase();

        row.style.display =
            text.includes(searchValue) ? "" : "none";

    });
}


/* =========================================================
   BILLING
========================================================= */

function openAddBillModal() {

    openModal("addBillModal");

    setDefaultBillDate();
}


function closeAddBillModal() {
    closeModal("addBillModal");
}


/* Set today's date when creating a bill */

function setDefaultBillDate() {

    const billDate = document.getElementById("billDate");

    if (!billDate) {
        return;
    }

    if (!billDate.value) {

        const today = new Date();

        const year = today.getFullYear();

        const month = String(
            today.getMonth() + 1
        ).padStart(2, "0");

        const day = String(
            today.getDate()
        ).padStart(2, "0");

        billDate.value =
            year + "-" + month + "-" + day;
    }
}


/* View bill */

function viewBill(
    id,
    patientName,
    treatment,
    amount,
    billDate,
    dueDate,
    paymentMethod,
    status
) {

    document.getElementById("viewBillAvatar").textContent =
        patientName
            ? patientName.charAt(0).toUpperCase()
            : "B";

    document.getElementById("viewBillPatient").textContent =
        patientName || "-";

    document.getElementById("viewBillId").textContent =
        "#" + id;

    document.getElementById("viewBillTreatment").textContent =
        treatment || "-";

    document.getElementById("viewBillAmount").textContent =
        "₹" + formatAmount(amount);

    document.getElementById("viewBillDate").textContent =
        billDate || "-";

    document.getElementById("viewBillDueDate").textContent =
        dueDate || "-";

    document.getElementById("viewBillPaymentMethod").textContent =
        paymentMethod || "-";

    document.getElementById("viewBillStatus").textContent =
        status || "-";

    openModal("viewBillModal");
}


function closeViewBillModal() {
    closeModal("viewBillModal");
}


/* Edit bill */

function editBill(
    id,
    patientName,
    treatment,
    amount,
    billDate,
    dueDate,
    paymentMethod,
    status
) {

    document.getElementById("editBillForm").action =
        "/edit_bill/" + id;

    document.getElementById("editBillPatient").value =
        patientName || "";

    document.getElementById("editBillTreatment").value =
        treatment || "";

    document.getElementById("editBillAmount").value =
        amount || 0;

    document.getElementById("editBillDate").value =
        billDate || "";

    document.getElementById("editBillDueDate").value =
        dueDate || "";

    document.getElementById("editBillPaymentMethod").value =
        paymentMethod || "";

    document.getElementById("editBillStatus").value =
        status || "Unpaid";

    openModal("editBillModal");
}


function closeEditBillModal() {
    closeModal("editBillModal");
}


/* Format amount */

function formatAmount(amount) {

    const number = Number(amount);

    if (Number.isNaN(number)) {
        return "0.00";
    }

    return number.toFixed(2);
}


/* Billing live search */

function filterBilling() {

    const input = document.getElementById("billingSearch");
    const table = document.getElementById("billingTable");

    if (!input || !table) {
        return;
    }

    const searchValue = input.value.toLowerCase().trim();
    const rows = table.querySelectorAll("tbody tr");

    rows.forEach(function (row) {

        const text = row.textContent.toLowerCase();

        row.style.display =
            text.includes(searchValue) ? "" : "none";

    });
}


/* =========================================================
   GLOBAL SEARCH PAGE
========================================================= */

function clearGlobalSearch() {

    const input = document.getElementById("globalSearch");

    if (input) {
        input.value = "";
    }

    window.location.href = "/search";
}


/* =========================================================
   QUICK ACTIONS
========================================================= */

function goToPatients() {
    window.location.href = "/patients";
}


function goToDoctors() {
    window.location.href = "/doctors";
}


function goToAppointments() {
    window.location.href = "/appointments";
}


function goToBilling() {
    window.location.href = "/billing";
}


/* =========================================================
   DATE VALIDATION
========================================================= */

/* Make sure due date is not before bill date */

document.addEventListener("DOMContentLoaded", function () {

    const billDate = document.getElementById("billDate");
    const dueDate = document.getElementById("billDueDate");

    if (billDate && dueDate) {

        billDate.addEventListener("change", function () {

            dueDate.min = billDate.value;

        });

    }


    const editBillDate =
        document.getElementById("editBillDate");

    const editBillDueDate =
        document.getElementById("editBillDueDate");

    if (editBillDate && editBillDueDate) {

        editBillDate.addEventListener(
            "change",
            function () {

                editBillDueDate.min =
                    editBillDate.value;

            }
        );

    }

});


/* =========================================================
   FORM SUBMISSION PROTECTION
========================================================= */

document.addEventListener("submit", function (event) {

    const form = event.target;

    if (!form) {
        return;
    }

    const submitButton =
        form.querySelector('button[type="submit"]');

    if (submitButton) {

        submitButton.dataset.originalText =
            submitButton.innerHTML;

        submitButton.disabled = true;

        submitButton.style.opacity = "0.7";

    }

});


/* =========================================================
   INITIALIZATION
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /*
       Set today's date when the billing page
       contains the Add Bill modal.
    */

    const addBillModal =
        document.getElementById("addBillModal");

    if (addBillModal) {
        setDefaultBillDate();
    }

});