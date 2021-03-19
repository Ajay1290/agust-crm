// Deal with displaying coupon information.
var coupons = function () {
  var durationSelector = '#duration';
  var durationInMonths = '#duration-in-months';
  var redeemBy = '#redeem_by';
  
  var $duration = $(durationSelector);
  var $durationInMonths = $(durationInMonths);
  var $redeemBy = $(redeemBy);
  
  $('body').on('change', durationSelector, function () {
    if ($duration.val() === 'repeating') {
      $durationInMonths.show();
    }
    else {
      $durationInMonths.hide();
    }
  });

  if ($redeemBy.length) {
    $redeemBy.datetimepicker({
      widgetParent: '.dt',
      format: 'YYYY-MM-DD HH:mm:ss',
      icons: {
        time: 'fa fa-clock-o',
        date: 'fa fa-calendar',
        up: 'fa fa-arrow-up',
        down: 'fa fa-arrow-down',
        previous: 'fa fa-chevron-left',
        next: 'fa fa-chevron-right',
        clear: 'fa fa-trash'
      }
    });
  }
};
