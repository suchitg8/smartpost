		(function($) {
			var g_skipper;
			var wizard = $("#wizard").steps({
				onStepChanging: function(event, currentIndex, newIndex) {
					console.log(currentIndex); 
					var skipper = $("#wizard > div.actions.clearfix > ul > li:nth-child(2) > a"); 
					g_skipper = skipper;
					var ok=true;
					$("#wizard-p-"+currentIndex+" input").each(function() {
						ok = validator.element(this);
					}); 
					if(newIndex >= 5 && ok) {
						skipper.addClass("skip");
						skipper.text("Skip this step");
					} else {
						skipper.removeClass("skip"); 
						skipper.text("Continue");
					}
					return ok;
				}
			});
			$("input[type=range]").each(function() {
				$(this).next().children().first().slider({
					range: "min", 
					min: 1,
					value: 2,
					max: 6, 
					slide: function(event, ui) {
						$(this).parent().prev().val(ui.value); 
					}
				}); 
				$(this).val($(this).next().children().first().slider("value")); 
			}); 
			var validator = $("#form-id").validate();
			$(".sixth-step .plan-box").click(function() {
				$("#plan-type").val($(this).parent().prevAll().length - 3);
				console.log($(this).parent().prevAll().length - 3);
				g_skipper.click();
			}); 
		})(jQuery); 
