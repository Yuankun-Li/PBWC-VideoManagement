/**
 * 
 */
	
$(document).ready(function(){
	$('#id_le_officer').hide();
	$("label[for='id_le_officer']").hide();
	$('#id_le_report').hide();
	$("label[for='id_le_report']").hide();
	$('#id_le_recorder').hide();
	$("label[for='id_le_recorder']").hide();
	$('#id_le_superior').hide();
	$("label[for='id_le_superior']").hide();
	$('#id_le_misconduct').hide();
	$("label[for='id_le_misconduct']").hide();
	$('#id_legalrep_role').hide();
	$("label[for='id_legalrep_role']").hide();

  	$('#id_community_member').click(function(){
			$('#id_le_officer').prop('checked', false);
			$('#id_le_officer').toggle(this.checked);
			$("label[for='id_le_officer']").toggle(this.checked);
	});

  	$('#id_le_officer').click(function(){
			$('#id_le_report').prop('checked', false);
			$('#id_le_report').toggle(this.checked);
			$("label[for='id_le_report']").toggle(this.checked);
	});

  	$('#id_le_report').click(function(){
			$('#id_le_recorder').prop('checked', false);
			$('#id_le_superior').prop('checked', false);
			$('#id_le_recorder').toggle(this.checked);
			$("label[for='id_le_recorder']").toggle(this.checked);
			$('#id_le_superior').toggle(this.checked);
			$("label[for='id_le_superior']").toggle(this.checked);
	});

  	$('#id_le_superior').click(function(){
			$('#id_le_misconduct').prop('checked', false);
			$('#id_le_misconduct').toggle(this.checked);
			$("label[for='id_le_misconduct']").toggle(this.checked);
	});

  	$('#id_legalrep').click(function(){
			$('#id_legalrep_role>option:eq(0)').prop('selected', true);
			$('#id_legalrep_role').toggle(this.checked);
			$("label[for='id_legalrep_role']").toggle(this.checked);
	});

});

