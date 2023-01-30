import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import matplotlib.ticker as mticker
import pandas as pd
import copy

import cartopy.crs as ccrs
import cartopy.feature as cfeature


def get_precip_lvls_colors():
    lvls = np.array([0.2, 1, 2, 5, 10, 20, 50, 100, 150, 200])
    colors = np.array([
        [219, 216, 199], [220, 255, 200], [150, 255, 150], [100, 255, 255],
        [0, 200, 255], [0, 100, 255], [150, 100, 255], [220, 100, 255],
        [255, 0, 255], [255*2/3, 0, 255*2/3]])/255
    return lvls, colors


def init_fonts():
    rcParams.update({'font.family': 'serif'})
    rcParams.update({'font.serif': 'Liberation Serif'})
    rcParams.update({'mathtext.fontset': 'dejavuserif'})
    rcParams.update({'font.size': 9})


def setup_grid(ax, proj):
    grid = ax.gridlines(
        crs=proj, draw_labels=True,
        linewidth=1, color='gray', alpha=0.4, linestyle='--')

    grid.right_labels = False
    grid.top_labels = False
    grid.left_labels = False
    grid.bottom_labels = False

    grid.xlocator = mticker.FixedLocator(np.arange(-180, 180+10, 10))
    grid.ylocator = mticker.FixedLocator(np.arange(-90, 100, 10))

    ax.add_feature(
        cfeature.COASTLINE, linewidth=1,
        edgecolor=np.array([0.9375, 0.9375, 0.859375])/2)
    ax.add_feature(
        cfeature.BORDERS,
        edgecolor=np.array([0.9375, 0.9375, 0.859375])/2,
        linewidth=.5)


def create_colorbar(ax, con, lon=-177, lat=-10):
    cbbox = ax.inset_axes([lon, lat, 53, 11], transform=ax.transData)
    cbbox.set_facecolor([1, 1, 1, .7])
    [cbbox.spines[k].set_visible(False) for k in cbbox.spines]
    cbbox.axes.get_xaxis().set_visible(False)
    cbbox.axes.get_yaxis().set_visible(False)
    cbbox.set_xticklabels([])
    cbbox.set_xticks([])
    cbbox.set_yticklabels([])
    cbbox.set_yticks([])

    axin = ax.inset_axes([lon+2, lat+7, 50, 3], transform=ax.transData)
    cbar = plt.colorbar(
        con, orientation='horizontal', ax=ax, cax=axin)
    return cbar


def add_local_time(ax, time, tz_name, offset, lon, lat):
    local_time = time + np.timedelta64(offset, 'h')
    local_time_dt = pd.to_datetime(str(local_time))
    local_time_str = (
        local_time_dt.day_name()[:3] + ' '
        + local_time_dt.strftime('%d/%m/%Y %H:%M'))
    label = '{} [{}]'.format(local_time_str, tz_name)
    ax.text(
        lon, lat, label, ha='center', va='center', fontsize=9,
        backgroundcolor=[1, 1, 1, .7])


def gen_omniglobe_mslp_prcp_temp(gadi=True, i_min=1, i_max=240):

    last_fc = np.datetime64('today') - np.timedelta64(1, 'D')

    if gadi:
        base_path = '/g/data/wr45/ops_aps3/access-g/1/{}/0000/fc/sfc/'.format(
            str(last_fc).replace('-', ''))
    else:
        base_path = 'https://dapds00.nci.org.au/thredds/dodsC/'
        base_path += 'wr45/ops_aps3/access-g/1/{}/0000/fc/sfc/'.format(
            str(last_fc).replace('-', ''))

    field = 'mslp'
    mslp = xr.open_dataset(base_path + field + '.nc')[field]

    field = 'accum_prcp'
    prcp = xr.open_dataset(base_path + field + '.nc')[field]

    field = 'temp_scrn'
    temp = xr.open_dataset(base_path + field + '.nc')[field]

    lab_pos = []
    for i in np.arange(-170, 190, 45):
        lab_pos += list(zip(
            np.arange(i-5, i+5),
            np.array([-75, -60, -45, -30, -15, 15, 30, 45, 60, 75])))

    temp_lab_pos = []
    for i in np.arange(-170+15, 190+15, 45):
        temp_lab_pos += list(zip(
            np.arange(i-3, i+4),
            np.array([-85, -60, -30, -15, 15, 30, 60, 85])))

    # Omni Globe
    lvls, colors = get_precip_lvls_colors()

    mslp_lab_lvls = np.arange(840, 1120, 8)
    mslp_fmt = {p: '{} hPa'.format(p) for p in mslp_lab_lvls}

    temp_lvls = np.arange(-15, 60, 15)
    temp_fmt = {
        t: u'{}\u00B0C'.format(t) for t in temp_lvls}

    for i in np.arange(len(mslp.time.values))[i_min: i_max]:
        time = mslp.time.values[i]
        print('Plotting {}'.format(
            np.datetime_as_string(time, unit='m')))
        plt.close('all')

        proj = ccrs.PlateCarree()

        fig = plt.figure(figsize=(28, 14))
        ax = fig.add_subplot(1, 1, 1, projection=proj)

        init_fonts()

        # Setup Map
        setup_grid(ax, proj)
        ax.add_feature(cfeature.LAND)

        # Plot datasets
        mslp_i = mslp.sel(time=time)

        prcp_i = (prcp.isel(time=i)-prcp.isel(time=(i-1)))
        prcp_i = 3*prcp_i/997*1e3

        temp_i = temp.sel(time=time) - 273.15

        print('Plotting precipitation.')
        conp = ax.contourf(
            prcp_i.lon, prcp_i.lat, prcp_i, levels=lvls,
            extend='max', colors=colors[:-1], alpha=1)
        conp.cmap.set_over(colors[-1])
        conp.changed()

        # Setup colorbar
        cbar = create_colorbar(ax, conp)
        cbar.ax.set_xticklabels(
            ['0.2', '1', '2', '5', '10', '20', '50', '100', '150', '200'])
        cbar.ax.set_xlabel('Precipitation [mm/(3 h)]')

        print('Plotting MSLP.')
        con8 = ax.contour(
            mslp_i.lon, mslp_i.lat, mslp_i/1e2,
            levels=np.arange(840, 1120, 8), colors='k',
            linewidths=1)

        ax.clabel(
            con8, inline=True, fontsize=9, manual=lab_pos, fmt=mslp_fmt)

        print('Plotting temp.')

        cont = ax.contour(
            temp_i.lon, temp_i.lat, temp_i,
            levels=temp_lvls, cmap='plasma',
            linewidths=.5, linestyles='solid')

        ax.clabel(
            cont, inline=True, fontsize=9, manual=temp_lab_pos, fmt=temp_fmt)

        # Get local melbourne time - with daylight savings calculated!
        first_sunday_oct = np.busday_offset(
            str(time)[:5] + '10', 0, roll='forward', weekmask='Sun')
        first_sunday_apr = np.busday_offset(
            str(time)[:5] + '04', 0, roll='forward', weekmask='Sun')

        time_dt = pd.to_datetime(str(time))
        time_str = (
            time_dt.day_name()[:3] + ' ' + time_dt.strftime('%d/%m/%Y %H:%M'))

        if (
                time < (first_sunday_apr + np.timedelta64(2, 'h'))
                or time >= (first_sunday_oct + np.timedelta64(2, 'h'))):
            mel_tz = 'AEDT'
            mel_time = time + np.timedelta64(11, 'h')
        else:
            mel_tz = 'AEST'
            mel_time = time + np.timedelta64(10, 'h')

        mel_time_dt = pd.to_datetime(str(mel_time))
        mel_time_str = (
            mel_time_dt.day_name()[:3] + ' '
            + mel_time_dt.strftime('%d/%m/%Y %H:%M'))

        label = 'ACCESS-G t+{:03d} h \n {} [UTC]'.format(
            i+1, time_str, )
        label_aus = '{} [{}]'.format(mel_time_str, mel_tz)

        ax.text(
            -152, 1, label, ha='center', fontsize=9,
            backgroundcolor=[1, 1, 1, .7])
        ax.text(
            134, -25, label_aus, ha='center', va='center', fontsize=9,
            backgroundcolor=[1, 1, 1, .7])

        add_local_time(ax, time, 'MST', -7, -104, 40)
        add_local_time(ax, time, 'AST', -4, -60, -5)
        add_local_time(ax, time, 'WAT', 1, 16, 15)
        add_local_time(ax, time, 'NST', 7, 84, 55)

        ax.axis('off')

        print('Saving.')

        if gadi:
            save_dir = '/g/data/w40/esh563/chart_discussion_figs/ACCESS_G/'
        else:
            save_dir = './mslp_anim/'

        plt.savefig(
            save_dir + 'mslp_{:04d}.png'.format(i), bbox_inches='tight',
            facecolor='w', pad_inches=0, dpi=190)


def gen_omniglobe_wind_mslp(gadi=True, i_min=1, i_max=240):

    last_fc = np.datetime64('today') - np.timedelta64(1, 'D')

    if gadi:
        base_path = '/g/data/wr45/ops_aps3/access-g/1/{}/0000/fc/sfc/'.format(
            str(last_fc).replace('-', ''))
    else:
        base_path = 'https://dapds00.nci.org.au/thredds/dodsC/'
        base_path += 'wr45/ops_aps3/access-g/1/{}/0000/fc/sfc/'.format(
            str(last_fc).replace('-', ''))

    field = 'uwnd10m'
    u = xr.open_dataset(base_path + field + '.nc')[field]

    field = 'vwnd10m'
    v = xr.open_dataset(base_path + field + '.nc')[field]

    field = 'temp_scrn'
    temp = xr.open_dataset(base_path + field + '.nc')[field]

    field = 'mslp'
    mslp = xr.open_dataset(base_path + field + '.nc')[field]

    lab_pos = []
    for i in np.arange(-170, 190, 45):
        lab_pos += list(zip(
            np.arange(i-5, i+5),
            np.array([-75, -60, -45, -30, -15, 15, 30, 45, 60, 75])))

    temp_lab_pos = []
    for i in np.arange(-170+15, 190+15, 45):
        temp_lab_pos += list(zip(
            np.arange(i-3, i+4),
            np.array([-85, -60, -30, -15, 15, 30, 60, 85])))

    mslp_lab_lvls = np.arange(840, 1120, 8)
    mslp_fmt = {p: '{} hPa'.format(p) for p in mslp_lab_lvls}

    speed_lvls = np.arange(0, 40, 5)

    for i in np.arange(len(u.time.values))[i_min: i_max]:
        time = u.time.values[i]
        print('Plotting {}'.format(
            np.datetime_as_string(time, unit='m')))
        plt.close('all')

        proj = ccrs.PlateCarree()

        fig = plt.figure(figsize=(28, 14))
        ax = fig.add_subplot(1, 1, 1, projection=proj)

        init_fonts()

        # Plot datasets
        u_i = u.sel(time=time)
        v_i = v.sel(time=time)
        # v_i = v_i.interp_like(u_i)

        u_i_2 = copy.deepcopy(u_i)
        v_i_2 = copy.deepcopy(v_i)
        u_i_2['lon'] = u_i_2.lon - 360
        v_i_2['lon'] = v_i_2.lon - 360

        u_i = xr.concat([u_i_2, u_i], dim='lon')
        v_i = xr.concat([v_i_2, v_i], dim='lon')

        new_lon = np.arange(-180, 180+0.2, 0.2)
        new_lat = np.arange(-90, 90+0.2, 0.2)

        u_i = u_i.interp(
            lon=new_lon, lat=new_lat, kwargs={'fill_value': 'extrapolate'})
        v_i = v_i.interp(
            lon=new_lon, lat=new_lat, kwargs={'fill_value': 'extrapolate'})
        # Note getting arrow size and spacing correct harder that it seems!

        speed_i = np.sqrt(u_i**2+v_i**2)

        print('Plotting winds.')
        conw = ax.contourf(
            speed_i.lon, speed_i.lat, speed_i, levels=speed_lvls,
            extend='max', cmap='Reds', alpha=1)

        cbar = create_colorbar(ax, conw)

        cbar.ax.set_xticklabels(speed_lvls)
        cbar.ax.set_xlabel('Wind Speed [m/s]')

        # Setup Map
        setup_grid(ax, proj)

        space = 15
        ax.quiver(
            u_i.lon[::space], u_i.lat[::space],
            u_i[::space, ::space], v_i[::space, ::space],
            scale=360*8, scale_units='width', width=5e-4,
            transform=proj)

        print('Plotting MSLP.')
        mslp_i = mslp.sel(time=time)
        con8 = ax.contour(
            mslp_i.lon, mslp_i.lat, mslp_i/1e2,
            levels=np.arange(840, 1120, 8), colors='k',
            linewidths=.5, alpha=.5)

        ax.clabel(
            con8, inline=True, fontsize=9, manual=lab_pos, fmt=mslp_fmt)

        # Get local melbourne time - with daylight savings calculated!
        first_sunday_oct = np.busday_offset(
            str(time)[:5] + '10', 0, roll='forward', weekmask='Sun')
        first_sunday_apr = np.busday_offset(
            str(time)[:5] + '04', 0, roll='forward', weekmask='Sun')

        time_dt = pd.to_datetime(str(time))
        time_str = (
            time_dt.day_name()[:3] + ' ' + time_dt.strftime('%d/%m/%Y %H:%M'))

        if (
                time < (first_sunday_apr + np.timedelta64(2, 'h'))
                or time >= (first_sunday_oct + np.timedelta64(2, 'h'))):
            mel_tz = 'AEDT'
            mel_time = time + np.timedelta64(11, 'h')
        else:
            mel_tz = 'AEST'
            mel_time = time + np.timedelta64(10, 'h')

        mel_time_dt = pd.to_datetime(str(mel_time))
        mel_time_str = (
            mel_time_dt.day_name()[:3] + ' '
            + mel_time_dt.strftime('%d/%m/%Y %H:%M'))

        label = 'ACCESS-G t+{:03d} h \n {} [UTC]'.format(
            i+1, time_str, )
        label_aus = '{} [{}]'.format(mel_time_str, mel_tz)

        ax.text(
            -152, 1, label, ha='center', fontsize=9,
            backgroundcolor=[1, 1, 1, .7])
        ax.text(
            134, -25, label_aus, ha='center', va='center', fontsize=9,
            backgroundcolor=[1, 1, 1, .7])

        add_local_time(ax, time, 'MST', -7, -104, 40)
        add_local_time(ax, time, 'AST', -4, -60, -5)
        add_local_time(ax, time, 'WAT', 1, 16, 15)
        add_local_time(ax, time, 'NST', 7, 84, 55)

        ax.axis('off')

        print('Saving.')

        if gadi:
            save_dir = '/g/data/w40/esh563/chart_discussion_figs/'
            save_dir += 'ACCESS_G_wind/'
        else:
            save_dir = './wind_anim/'

        plt.savefig(
            save_dir + 'wind_{:04d}.png'.format(i), bbox_inches='tight',
            facecolor='w', pad_inches=0, dpi=190)
