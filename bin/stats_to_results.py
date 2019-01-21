from analysis.StatAndMatch import StatMatchAggregator, StatMatchLinRegAnalyzer

def stats_to_results():
    stat_match_agg = StatMatchAggregator()
    #stat_match_data = stat_match_agg.get_results_by_stat_match_type_and_team()
    #stat_match_data.plot_data()

    separate_by_team = True
    stat_match_lin_reg = StatMatchLinRegAnalyzer(stat_match_agg.get_results_by_stat_and_match_type(separate_by_team))
    lin_reg_data = stat_match_lin_reg.get_transformed_data()
    for stat in lin_reg_data.keys():
        for match_type in lin_reg_data[stat].keys():
            if not separate_by_team:
                r_squared = lin_reg_data[stat][match_type][2]**2
                print 'r-squared for {} vs {} results: {}'.format(stat, match_type, r_squared)
            else:
                for team_name in lin_reg_data[stat][match_type].keys():
                    r_squared = lin_reg_data[stat][match_type][team_name][2]**2
                    print 'r-squared for {} vs {} results ({}): {}'.format(stat, match_type, team_name, r_squared)

    #print 'r-squared for {} vs {} results: {}'.format(stat, match_type, rvalue**2)
    #print 'r-squared for {} vs {} results ({}): {}'.format(stat, match_type, team_name, rvalue**2)

if __name__=="__main__":
    stats_to_results()
