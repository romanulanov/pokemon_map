from django.db import models  # noqa F401
from django.utils.timezone import now


class Pokemon(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Имя',
                             )
    title_en = models.CharField(max_length=200,
                                verbose_name='Имя по-английски',
                                blank=True)
    title_jp = models.CharField(max_length=200,
                                verbose_name='Имя по-японски',
                                blank=True)
    photo = models.ImageField(upload_to='images',
                              null=True,
                              blank=True,
                              verbose_name='Картинка')
    description = models.TextField(max_length=400,
                                   blank=True,
                                   verbose_name='Описание')
    previous_evolution = models.ForeignKey("self",
                                           verbose_name='Из кого эволюционирует',
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name='next_gen')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон', related_name='entities')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появится')
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет')
    level = models.IntegerField(blank=True,
                                verbose_name='Уровень',
                                null=True)
    health = models.IntegerField(blank=True,
                                 verbose_name='Здоровье',
                                 null=True)
    strength = models.IntegerField(blank=True,
                                   verbose_name='Атака',
                                   null=True)
    defence = models.IntegerField(blank=True,
                                  verbose_name='Защита',
                                  null=True)
    stamina = models.IntegerField(blank=True,
                                  verbose_name='Выносливость',
                                  null=True)
    def __str__(self):
        return f'{self.pokemon} - {self.pk}'
