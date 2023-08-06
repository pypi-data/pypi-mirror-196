from pipeline import PlotManager
import os
import pandas as pd
from reset import original_settings

if __name__ == '__main__':
    which_way = input("If you want to run the test version press 1. If you want to analyze your own data press 2.")
    if which_way == "1":
        test = True
    else:
        test = False
    if not os.path.isdir("results"):
        os.mkdir("results")
    else:
        pass
    result_dir = os.path.abspath("results")
    plot = PlotManager(test_version = test)
    folder_name = plot.experiment
    experiment_name = folder_name
    os.mkdir(os.path.join(result_dir, folder_name))
    os.mkdir(os.path.join(result_dir, folder_name, "Quality"))
    save_path = os.path.abspath(os.path.join(result_dir, folder_name, "Quality"))
    plot.settings_saver.change_save_path(path = save_path)
    plot.lengthDistribution_multi()
    plot.save(name = "length_Distribution" + folder_name)
    plot.logoPlot_multi()
    plot.save(name = "logo Plots " + folder_name)
    usq_multiple = input("The program wants to create the usq Plots. Do you want to include multiple samples in one usq plot? For instance if you have a library you can include multiple samples. Press Y or n")
    unique_experiments = list(plot.unique_experiments.values())
    if usq_multiple.lower() in ["Y", "y"]:
        more_plots = True
        while more_plots == True:
            print("Choose the sample from the list below which you want to include. Please seperate your input with commas")
            plot.print_samples()
            sample_names = input()
            if not type(sample_names) == list:
                sample_names = sample_names.split(",")
                sample_names = [value.replace("'", "").replace('"', '') for value in sample_names]
                sample_names = [value.replace(" ", "") for value in sample_names]
                sample_names = [value for value in sample_names if value]
            else:
                pass
            for value in sample_names:
                if value not in unique_experiments:
                    interrupt = input("The system could not find " + value + " in your sample name. If you want to try again, press Y. Otherwise the analysis will be conducted without this value")
                    if interrupt.lower() in ["Y", "y"]:
                        break
                    else:
                        sample_names.remove(value)
            plot.usqPlot(samples = sample_names)
            while True:
                usq_name = input("How do you want to call your USQ Plot?")
                if not os.path.isfile(os.path.join(save_path, usq_name)):
                    plot.save(usq_name)
                    break
                else:
                    print("The file already exists. Please try another value.")
            more_plots = input("Do you want to create more USQ Plots with different samples? (Y/n)")
            if more_plots.lower() in ["Y", "y"]:
                more_plots = True
                unique_experiments = [value for value in unique_experiments if value not in sample_names]
            else:
                more_plots = False
                break
    else:
        for experiment in unique_experiments:
            try:
                plot.usqPlot(samples = [experiment])
                plot.save("Usq Plot " + experiment)
            except:
                print("A problem appeard for " + experiment + ". The USQ plot could not be created")
    unique_experiments = list(plot.unique_experiments.values())
    plot.morosita_horn()
    plot.save("morosita_horn_identity")
    plot.jaccard()
    plot.save("jaccard_identity")
    plot.sorensen()
    plot.save("Sorensen_Dice_identity")
    plot.relative()
    plot.save("Relative_Identity")

    os.mkdir(os.path.join(result_dir, folder_name, "Sequence Analysis"))
    for experiment in unique_experiments:
        try:
            os.mkdir(os.path.join(result_dir,folder_name, "Sequence Analysis", experiment))
            save_path = os.path.abspath(os.path.join("results", folder_name, "Sequence Analysis", experiment))
            plot.settings_saver.change_save_path(path = save_path)
            plot.logoPlot_single(experiment)
            plot.save("Logo Plot for " + experiment)
            plot.rel_seq_abundance(samples = [experiment])
            plot.save("Sequence Abundance for " + experiment)
     #      plot.basic_cluster(experiment)
      #      plot.save("Clustering based on Levenshtein Distance")
            try:
                plot.aa_distribution(experiment, region = [3, 8])
                plot.save("AA Distribution " + "in region 3 - 8")
            except:
                pass
            try:
                plot.aa_distribution(sample = experiment, region = [9, 14])
                plot.save("AA Distribution "+ "in region 9 - 14")
            except: pass
            try:
                plot.aa_distribution(sample = experiment, region = [15, 20])
                plot.save("AA Distribution " + "in region 15 - 20")
            except:
                pass

        except: pass

    if isinstance(plot.binding_data, pd.DataFrame) == True:
        print("You have binding data for the following Antigens")
        plot.print_antigens()
        all_antigens = plot.binding_data.columns.to_list()[1:-1]
        count_AG = input("If you want to create a TSNE Embedding for all Antigens press 1. If you want to select certain Antigens, press 2.")
        if count_AG == str(1):
            antigens = all_antigens
        else:
            print("Enter one or more antigen names of the list given above. Seperate them by comma!")
            antigens = input()
            if not type(antigens) == list:
                antigens = antigens.split(",")
                antigens = [value.replace("'", "").replace('"', '') for value in antigens]
                antigens = [value.replace(" ", "") for value in antigens]
            else:
                pass
            for value in antigens:
                if value not in all_antigens:
                    interrupt = input("The system could not find " + value + " in your sample name. If you want to try again, press Y. Otherwise the analysis will be conducted without this value")
                    if interrupt.lower() in ["Y", "y"]:
                        break
                    else:
                        antigens.remove(value)

        for antigen in antigens:
            os.mkdir(os.path.join(result_dir, folder_name, "Binding Analysis"))
            os.mkdir(os.path.join(result_dir, folder_name, "Binding Analysis", antigen))
            save_path = os.path.abspath(os.path.join("results", folder_name, "Binding Analysis", antigen))
            for experiment in unique_experiments:
                plot.tsne_cluster_AG(sample = experiment, toxins = [antigen], toxin_names = False)

    else:
        print("You have not given any binding data. So this part of the analysis has not been carried out.")
    original_settings()