from weathon.dl.registry.registry import Registry,build_from_cfg, default_group


LOSS = Registry('loss')


def build_loss(cfg,task_name:str=default_group, default_args=None):
    
    return build_from_cfg(cfg, LOSS, group_key=task_name, default_args=default_args)