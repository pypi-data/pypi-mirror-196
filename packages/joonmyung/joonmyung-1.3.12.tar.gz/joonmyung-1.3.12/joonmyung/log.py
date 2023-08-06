from joonmyung.draw import data2PIL
from joonmyung.utils import to_np
import wandb
import torch
import os
import re

class AverageMeter:
    ''' Computes and stores the average and current value. '''
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.val = 0.0
        self.avg = 0.0
        self.sum = 0.0
        self.count = 0

    def update(self, val: float, n: int = 1) -> None:
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
    def __str__(self):
        return "\
        end = time.time() \n\
        batch_time = AverageMeter() \n\
        batch_time.update(time.time() - end) \n\
        end = time.time() \n\
        avg_score = AverageMeter()\n\
        accuracy = 0.1\n\
        avg_score.update(accuracy)\n\
        losses = AverageMeter()\n\
        loss = 0\n\
        batch_size = 128\n\
        losses.update(loss.data.item(), batch_size)\n\
        print(f'time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'\n\
              f'loss {losses.val:.4f} ({losses.avg:.4f})\t' \n\
              f'acc {avg_score.val:.4f} ({avg_score.avg:.4f})')"


class Logger():
    loggers = {}
    def __init__(self, use_wandb=True, wandb_entity=None, wandb_project=None, wandb_name=None
                 , wandb_watch=False, main_process=True, wandb_id=None, wandb_dir='./'
                 , args=None, model=False
                 , save=True):
        self.use_wandb = use_wandb and main_process

        if self.use_wandb:
            wandb.init(entity=wandb_entity, project=wandb_project, name=wandb_name
                       , resume="allow", id = wandb_id, dir=os.path.join(wandb_dir, 'wandb')
                       , config=args)

            if args: args.wandb_id = wandb.config.id = wandb.run.id
            if wandb_watch and model: wandb.watch(model, log='all')
            if save and args: torch.save({'args': args, }, os.path.join(wandb.run.dir, "args.pt"))

    def getLog(self, k, return_type =None):
        if return_type == "avg":
            return self.loggers[k].avg
        elif return_type == "val":
            return self.loggers[k].val
        else:
            return self.loggers[k]

    def delLog(self, columns: list):
        for column in columns:
            self.loggers.pop(column)

    def resetLog(self):
        self.loggers = {k:AverageMeter() if type(v) == AverageMeter else v for k, v in self.loggers.items()}

    def addLog(self, datas:dict, epoch=None, mae_task_type = None, bs = 1):
        for k, v in datas.items():
            data_type = v[0]
            if data_type == 0:  # Values
                self.loggers[k] = v[1]
            elif data_type == 1: # AverageMeter
                if k not in self.loggers.keys():
                    self.loggers[k] = AverageMeter()
                self.loggers[k].update(v[1], bs)
            elif data_type == 2: # Table
                columns = list(v[1].keys())
                data_num = len(list(v[1].values())[0])
                self.loggers[k] = wandb.Table(columns=["epoch", "MTT"] + columns)
                for idx in range(data_num):
                    self.loggers[k].add_data(str(epoch), str(mae_task_type), *[wandb.Image(to_np(data2PIL(v[1][k][idx]))) if len(v[1][k].shape) == 4 else to_np(v[1][k])[idx] for k in columns])
        return True

    def getPath(self):
        return wandb.run.dir

    def logWandb(self):
        if self.use_wandb:
            wandb.log({k:v.avg if type(v) == AverageMeter else v for k, v in self.loggers.items()})
            self.resetLog()
        else:
            print("Wandb is not Working Now")

    def finish(self):
        wandb.finish()

if __name__ == "__main__":
    from playground.analysis.lib_import import *
    dataset_name, server, device = "imagenet", "148", "cuda"
    data_path, _ = data2path(server, dataset_name)
    data_num = [[5, 1],
                [5, 2],
                [5, 3],
                [5, 4]]
    dataset = JDataset(data_path, dataset_name, device=device)
    samples, targets, imgs, label_names = dataset.getItems(data_num)

    logger = Logger(use_wandb=True, wandb_entity="joonmyung", wandb_project="test", wandb_name="AAPP",
                    wandb_watch=False, wandb_dir="./")

    logger.addLog({ "sample A": [0, 4],
                    "sample B": [0, 3],
                    "sample C": [0, 2],
                    "table  B": [2, {"image" :     samples, "prediction": targets}]})
    logger.logWandb()

    logger.finish()