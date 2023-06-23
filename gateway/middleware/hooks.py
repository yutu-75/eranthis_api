from gateway.middleware.check_params import check_params


def set_app_hook(app):
    """
    设置应用(app)钩子(before)
    :param app: app实例
    :return:
    """

    @app.before_first_request
    def before_first_request():
        pass

    # @app.before_request
    # def before_request():
    #     res = check_params()
    #     if res:
    #         return res

    @app.after_request
    def after_request(response):
        return response
