/**
 * 
 */
	
$(document).ready(function(){
	$('#id_le_trainingpurpose').hide();
	$("label[for='id_le_trainingpurpose']").hide();
	$('#id_le_Evidexculp').hide();
	$("label[for='id_le_Evidexculp']").hide();
	$('#id_le_role').hide();
	$("label[for='id_le_role']").hide();

  	$('#id_le_officer').click(function(){
			$('#id_le_trainingpurpose').toggle(this.checked);
			$("label[for='id_le_trainingpurpose']").toggle(this.checked);
			$('#id_le_Evidexculp').toggle(this.checked);
			$("label[for='id_le_Evidexculp']").toggle(this.checked);
  			$('#id_le_Evidexculp').click(function(){
				$('#id_le_role').toggle(this.checked);
				$("label[for='id_le_role']").toggle(this.checked);
			});

	});

});
