/**
 * User: bluven
 * Date: 15-7-7
 * Time: 下午5:45
 */
CloudApp.controller('InitWizardController',
    function($rootScope, $scope, $i18next, $timeout, $window,
             CommonHttpService, ToastrService, InitWizard){

        $scope.$on('$includeContentLoaded', function(){
                Metronic.initAjax();
                InitWizard.init()
        });

        $rootScope.settings.layout.pageBodySolid = true;
        $rootScope.settings.layout.pageSidebarClosed = false;

        var data_center = $scope.data_center = {auth_url: 'http://'},
            flavor = $scope.flavor = {},
            image = $scope.image = {};

        $scope.os_types = [{key: 1, label: 'Windows'}, {key: 2, label: 'Linux'}];

        $scope.submit = function(){
            var params = {};
            angular.extend(params, data_center);
            angular.extend(params, flavor);
            angular.extend(params, image);
            params.data_center_name = data_center.name;
            params.flavor_name = flavor.name;
            params.image_name = image.name;

            CommonHttpService.post('/api/init/', params).then(function(data){
                if (data.success) {

                    $timeout(function(){
                        $window.location.href = '/management/';
                    }, 5000);

                    bootbox.dialog({
                        'title': $i18next("success"),
                        message: '初始化已成功，页面会自动跳转到管理界面，您也可以点击<a href="javascript: overview();">这里</a>直接进入管理界面。'
                    });
                } else {
                    ToastrService.error(data.msg, $i18next("op_failed"));
                }
            });
        };
    })
    .factory('InitWizard', ['InitWizardValidator', function (InitWizardValidator) {

        var handleTitle = function(tab, navigation, index) {

            var total = navigation.find('li').length;
            var current = index + 1;
            // set wizard title
            $('.step-title', $('#cloud-wizard')).text((index + 1) + ' / ' + total);
            // set done steps
            jQuery('li', $('#cloud-wizard')).removeClass("done");
            var li_list = navigation.find('li');
            for (var i = 0; i < index; i++) {
                jQuery(li_list[i]).addClass("done");
            }

            if (current == 1) {
                $('#cloud-wizard').find('.button-previous').hide();
            } else {
                $('#cloud-wizard').find('.button-previous').show();
            }

            if (current >= total) {
                $('#cloud-wizard').find('.button-next').hide();
                $('#cloud-wizard').find('.button-submit').show();
            } else {
                $('#cloud-wizard').find('.button-next').show();
                $('#cloud-wizard').find('.button-submit').hide();
            }

            Metronic.scrollTo($('.page-title'));
        };

        var init = function(){

            if (!jQuery().bootstrapWizard) {
                return;
            }

            var form = InitWizardValidator.init();

            // default form wizard
            $('#cloud-wizard').bootstrapWizard({
                'nextSelector': '.button-next',
                'previousSelector': '.button-previous',
                onTabClick: function () { return false; },
                onNext: function (tab, navigation, index) {

                    if (form.valid() == false) {
                        return false;
                    }
                    handleTitle(tab, navigation, index);
                },
                onPrevious: function (tab, navigation, index) {
                    handleTitle(tab, navigation, index);
                },
                onTabShow: function (tab, navigation, index) {
                    var total = navigation.find('li').length;
                    var current = index + 1;
                    var $percent = (current / total) * 100;
                    $('#cloud-wizard').find('.progress-bar').css({
                        width: $percent + '%'
                    });
                }
            });

            $('#cloud-wizard').find('.button-previous').hide();
            $('#cloud-wizard .button-submit').hide();
        };

        return {init: init}
    }]).factory('InitWizardValidator',
        ['$i18next', 'ValidationTool', function ($i18next, ValidationTool){

        var dataCenterRules = {
                data_center_name: {
                    minlength: 2,
                    maxlength: 128,
                    required: true
                },
                host: {
                    required: true,
                    ip: true,
                    remote: {
                        url: "/api/data-centers/is-host-unique",
                        data: {},
                        async: false
                    }
                },
                project: {
                    required: true,
                    minlength: 2,
                    maxlength: 128
                },
                user: {
                    required: true,
                    minlength: 2,
                    maxlength: 128
                },
                password: {
                    required: true,
                    minlength: 2,
                    maxlength: 50
                },
                auth_url: {
                    required: true,
                    url: true
                },
                ext_net: {
                    required: true,
                    minlength: 2,
                    maxlength: 128
                }
            },
            flavorRules = {
                flavor_name: {
                    minlength: 2,
                    maxlength: 128,
                    required: true
                },
                cpu: {
                    required: true,
                    digits: true
                },
                memory: {
                    required: true,
                    digits: true
                },
                price: {
                    required: true,
                    number: true
                }
            },
            imageRules = {
                image_name: {
                    minlength: 2,
                    maxlength: 50,
                    required: true
                },
                os_type: 'required',
                login_name: 'required'
            },
            rules = {};

        angular.extend(rules, dataCenterRules);
        angular.extend(rules, flavorRules);
        angular.extend(rules, imageRules);

        var config = {
            rules: rules,
            messages: {
                host: {
                    remote: $i18next('data_center.host_is_used')
                }
            }
        };

        return {init: function(){
            return ValidationTool.init("#wizardForm", config);
        }};

    }]);