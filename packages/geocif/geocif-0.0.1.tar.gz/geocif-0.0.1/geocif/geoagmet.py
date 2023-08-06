import os

import arrow as ar
import pandas as pd
from tqdm import tqdm

from geocif import geocif, plot, utils


def create_title_for_plot(obj):
    region_name = obj.region.replace('_', ' ').title()
    calendar_region_name = obj.calendar_region.replace('_', ' ').title()
    country_name = obj.country.replace('_', ' ').title()
    long_crop_name = utils.get_crop_name(obj.crop)

    # Get name of crop based on metadata/crop_per_season.csv file
    df_crop_per_season = pd.read_csv(obj.dir_metadata / 'crop_per_season.csv')

    crop_name = df_crop_per_season[(df_crop_per_season['country'] == obj.country) &
                                   (df_crop_per_season['crop'] == obj.crop) &
                                   (df_crop_per_season['season'] == int(obj.growing_season))]['name'].values

    crop_name = crop_name[0] if crop_name else long_crop_name.replace('_', ' ').title()

    title_line_1 = f"{region_name} ({calendar_region_name}, {country_name})"
    title_line_2 = f"{crop_name} {obj.plot_season}"

    sup_title = f'{title_line_1}\n{title_line_2}'

    return sup_title


def plot_agmet(obj):
    # Get crop calendar dates for region
    dates_calendar = [obj.date_planting, obj.date_greenup, obj.date_senescence, obj.date_harvesting]

    # TODO: Only plot if dates_calendar has valid dates
    # Create title for plot
    sup_title = create_title_for_plot(obj)

    # Admin_1 level plots
    plot.plots_ts_cur_yr(obj.df_region,
                         obj.eo_plot,
                         closest=obj.closest,
                         dates_cal=dates_calendar,
                         frcast_yr=obj.plot_season,
                         logos=[obj.logo_harvest, obj.logo_geoglam],
                         dir_out=obj.dir_output / obj.scale,
                         sup_title=sup_title,
                         fname=f'{obj.region}.png')

    if obj.category == 'ewcm':
        columns_v2 = ['cumulative_precip', 'daily_precip', 'soil_moisture_as1']
        plot.plots_ts_cur_yr_v2(obj.df_region,
                                columns_v2,
                                closest=obj.closest,
                                dates_cal=dates_calendar,
                                frcast_yr=obj.plot_season,
                                dir_out=obj.dir_condition / 'v2' / 'admin_1',
                                sup_title=sup_title,
                                sname_crop=obj.crop,
                                fname=f'{obj.region}.png')

        columns_v3 = ['cumulative_precip', 'ndvi', 'soil_moisture_as1']
        plot.plots_ts_cur_yr_v3(obj.df_region,
                                columns_v3,
                                closest=obj.closest,
                                dates_cal=dates_calendar,
                                frcast_yr=obj.plot_season,
                                dir_out=obj.dir_condition / 'v2' / 'admin_1',
                                sup_title=sup_title,
                                sname_crop=obj.crop,
                                fname=f'{obj.region}.png')


def loop_agmet(path_config_file=None):
    """
    Args:
    """
    # Create GeoCif object
    obj = geocif.GeoCif(path_config_file)

    # Parse configuration files
    obj.parse_config()

    # Read in statistics: area, yield, production, metadata
    obj.read_statistics()

    # Create combinations of run parameters
    all_combinations = obj.create_run_combinations()

    pbar = tqdm(all_combinations, total=len(all_combinations))
    for country, scale, crop, growing_season in pbar:
        # Setup country information
        obj.setup_country(country, scale, crop, growing_season)

        # Loop through seasons and plot for each admin_1 region and calendar region
        for plot_season in obj.plot_seasons:
            # Get list of the years that are closest to the year which we want to plot
            obj.get_closest_season(plot_season)

            for region in obj.list_regions:
                # Setup the region information
                obj.setup_region(region, plot_season, 'region')

                # If available, add CHIRPS-GEFS data to the dataframe
                if obj.precip_var == 'chirps':
                    obj.add_precip_forecast(plot_season)

                # Get crop calendar dates for region
                dates_calendar = [obj.date_planting, obj.date_greenup, obj.date_senescence, obj.date_harvesting]

                # TODO: Only plot if dates_calendar has valid dates
                # Create title for plot
                sup_title = create_title_for_plot(obj)

                ###############################################################
                # Agmet plots for regions
                ###############################################################
                plot.plots_ts_cur_yr(obj.df_region,
                                     obj.eo_plot,
                                     closest=obj.closest,
                                     dates_cal=dates_calendar,
                                     frcast_yr=obj.plot_season,
                                     logos=[obj.logo_harvest, obj.logo_geoglam],
                                     dir_out=obj.dir_output / obj.scale,
                                     sup_title=sup_title,
                                     fname=f'{obj.region}.png')

                ###############################################################
                # Agmet plots for calendar regions
                ###############################################################
                columns = obj.eo_model + ['month', 'day', 'yield']
                if 'chirps' in obj.df_region.columns:
                    bool_year_check, bool_date_check = obj.check_date(obj.df_region, obj.plot_season)

                    if bool_date_check and bool_year_check:
                        columns = obj.eo_plot + ['month', 'day', 'chirps_gefs', 'yield']

                df_calendar_region = obj.df_region.groupby(['country', 'calendar_region', 'harvest_season', 'doy', 'datetime'])[columns].mean().reset_index()
                df_calendar_region.set_index(pd.DatetimeIndex(df_calendar_region['datetime']), inplace=True, drop=True)
                df_calendar_region.index.name = None
                df_calendar_region.sort_values(by='datetime', inplace=True)

                # TODO: Only plot if dates_calendar has valid dates
                # Create title for plot
                sup_title = create_title_for_plot(obj)

                if not df_calendar_region.empty:
                    plot.plots_ts_cur_yr(df_calendar_region,
                                         obj.eo_plot,
                                         closest=obj.closest,
                                         dates_cal=dates_calendar,
                                         frcast_yr=obj.plot_season,
                                         logos=[obj.logo_harvest, obj.logo_geoglam],
                                         dir_out=obj.dir_output / 'district',
                                         sup_title=sup_title,
                                         fname=f'{obj.calendar_region}.png')


def run():
    loop_agmet(['D:/Users/ritvik/projects/geoprepare/geoprepare/geoprepare.txt',
                'D:/Users/ritvik/projects/geoprepare/geoprepare/geoextract.txt',
                'D:/Users/ritvik/projects/geocif/geocif/config/geocif.txt'])


if __name__ == '__main__':
    run()
