# plot_helper.py

import matplotlib.pyplot as plt
import matplotlib as mpl
import os


class PlotHelper:
    """Utilities for plotting graphs"""

    @staticmethod
    def basic_train_val_plot_and_save(title, train_data, validation_data, legend_location, output_dir):
        """Plot pairs of datasets

        :param title: str -- figure title, used as base for saved file name
        :param train_data: dataset -- training results
        :param validation_data: dataset -- validation results
        :param legend_location: str -- location of legend on the Figure e.g. 'upper right'
        :param output_dir: str -- target directory for saving plot
        """

        plt.plot(train_data, color='b', label='Training')
        plt.plot(validation_data, color='g', label='Validation')
        plt.title(title)
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Training', 'Validation'], loc=legend_location)
        plt.grid()

        target_path = os.path.join(output_dir, title.replace(' ', '_')+'.svg')
        # If use plt.show() before saving, then saved figure is blank. Works ok other way round.
        plt.savefig(target_path)

        # plt.show()

    @staticmethod
    def basic_run_plot(bce_loss_train, total_loss_train, bce_loss_val, total_loss_val, output_dir):
        PlotHelper.basic_train_val_plot_and_save(
            # style='seaborn',
            title='BCE Loss',
            train_data=bce_loss_train,
            validation_data=bce_loss_val,
            legend_location='upper right',
            output_dir=output_dir)

        PlotHelper.basic_train_val_plot_and_save(
            title='Total Loss',
            train_data=total_loss_train,
            validation_data=total_loss_val,
            legend_location='upper right',
            output_dir=output_dir)
