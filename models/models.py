from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

""" models generated using sqlacodegen library """


class TblPlayer(Base):
    __tablename__ = 'tbl_player'

    int_player_id = Column(Integer, primary_key=True)
    str_player_name = Column(String(120))

    def __repr__(self) -> str:
        return super().__repr__()

    str_positions = Column(String(120))
    dt_date_of_birth = Column(Date)
    int_height = Column(Integer)
    int_weight = Column(Integer)
    int_overall_rating = Column(Integer)
    int_potential_rating = Column(Integer)
    str_best_position = Column(String(120))
    int_best_overall_rating = Column(Integer)
    int_value = Column(Integer)
    int_wage = Column(Integer)
    str_player_image_url = Column(String(255))
    int_team_id = Column(Integer)
    str_nationality = Column(String(50))


class TblPlayerAttacking(Base):
    __tablename__ = 'tbl_player_attacking'

    int_attacking_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    int_crossing = Column(Integer)
    int_finishing = Column(Integer)
    int_heading_accuracy = Column(Integer)
    int_short_passing = Column(Integer)
    int_volleys = Column(Integer)


class TblPlayerDefending(Base):
    __tablename__ = 'tbl_player_defending'

    int_defending_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    int_defensive_awareness = Column(Integer)
    int_standing_tackle = Column(Integer)
    int_sliding_tackle = Column(Integer)


class TblPlayerGoalkeeping(Base):
    __tablename__ = 'tbl_player_goalkeeping'

    int_goalkeeping_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    int_diving = Column(Integer)
    int_handling = Column(Integer)
    int_kicking = Column(Integer)
    int_positioning = Column(Integer)
    int_reflexes = Column(Integer)


class TblPlayerMentality(Base):
    __tablename__ = 'tbl_player_mentality'

    int_mentality_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    int_aggression = Column(Integer)
    int_interceptions = Column(Integer)
    int_positioning = Column(Integer)
    int_vision = Column(Integer)
    int_penalties = Column(Integer)
    int_composure = Column(Integer)


class TblPlayerMovement(Base):
    __tablename__ = 'tbl_player_movement'

    int_movement_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    int_acceleration = Column(Integer)
    int_sprint_speed = Column(Integer)
    int_agility = Column(Integer)
    int_reactions = Column(Integer)
    int_balance = Column(Integer)


class TblPlayerPower(Base):
    __tablename__ = 'tbl_player_power'

    int_power_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    int_shot_power = Column(Integer)
    int_jumping = Column(Integer)
    int_stamina = Column(Integer)
    int_strength = Column(Integer)
    int_long_shots = Column(Integer)


class TblPlayerProfile(Base):
    __tablename__ = 'tbl_player_profile'

    int_profile_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    str_preferred_foot = Column(String(20))
    int_weak_foot = Column(Integer)
    int_skill_moves = Column(Integer)
    int_international_reputations = Column(Integer)
    str_work_rate = Column(String(100))
    str_body_type = Column(String(100))


class TblPlayerSkill(Base):
    __tablename__ = 'tbl_player_skill'

    int_skill_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    int_dribbling = Column(Integer)
    int_curve = Column(Integer)
    int_fk_accuracy = Column(Integer)
    int_long_passing = Column(Integer)
    int_ball_control = Column(Integer)


class TblPlayerSpeciality(Base):
    __tablename__ = 'tbl_player_specialities'

    int_speciality_id = Column(Integer, primary_key=True)
    int_player_id = Column(Integer, nullable=False)
    str_player_speciality = Column(String(150))


class TblPlayerTrait(Base):
    __tablename__ = 'tbl_player_traits'

    int_player_id = Column(Integer, nullable=False)
    str_trait = Column(String(150))
    int_trait_id = Column(Integer, primary_key=True)


class TblPlayerUrl(Base):
    __tablename__ = 'tbl_player_urls'

    int_player_id = Column(Integer, primary_key=True)
    str_url = Column(String(255), nullable=False)
    dt_crawled = Column(DateTime)


class TblTeamUrl(Base):
    __tablename__ = 'tbl_team_urls'

    int_team_id = Column(Integer, primary_key=True)
    str_url = Column(String(255), nullable=False)
    dt_crawled = Column(DateTime)


class TblTeam(Base):
    __tablename__ = 'tbl_team'

    int_team_id = Column(Integer, primary_key=True)
    str_team_name = Column(String(255), nullable=False)
    str_league = Column(String(255))
    int_overall = Column(Integer)
    int_attack = Column(Integer)
    int_midfield = Column(Integer)
    int_defence = Column(Integer)
    int_international_prestige = Column(Integer)
    int_domestic_prestige = Column(Integer)
    int_transfer_budget = Column(Integer)


class TblTeamTactic(Base):
    __tablename__ = 'tbl_team_tactics'

    int_tactic_id = Column(Integer, primary_key=True)
    int_team_id = Column(Integer, nullable=False)
    str_defensive_style = Column(String(255))
    int_team_width = Column(Integer)
    int_depth = Column(Integer)
    str_offensive_style = Column(String(255))
    int_width = Column(Integer)
    int_players_in_box = Column(Integer)
    int_corners = Column(Integer)
    int_freekicks = Column(Integer)
