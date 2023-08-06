import nni


class MetricsReporter(object):

    '''
    Update the new parameters
    '''
    @classmethod
    def update_report_params(cls, args):
        cfg = vars(args)
        params = nni.get_next_parameter()
        cfg.update(params)

    @classmethod
    def report_intermediate_result(self, val_acc):
        nni.report_intermediate_result(val_acc)

    @classmethod
    def report_final_result(self, final_acc):
        nni.report_final_result(final_acc)
